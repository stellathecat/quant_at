import sys; sys.path.append('..')
sys.path.append('../../data')
import pandas as pd
import scipy.stats, numpy as np
import futures, util

import Quandl, os, itertools, sys
from pymongo import MongoClient
import logging, datetime, simple
import pandas as pd, collections
import numpy as np, futures

def get_stitched(symbol, market):
    """
    Returns all data for symbol in a pandas dataframe
    """
    connection = MongoClient()
    db = connection.findb
    
    q = {"$query" :{"_id.sym": symbol, "_id.market": market},"$orderby":{"_id.dt" : 1}}
    res = list(db.sticon.find( q ))
    if len(res) == 0: return pd.DataFrame()
    tmp = []
    for x in res: tmp.append( { 'carrycont': x['carrycont'], 'effcont': x['effcont'],
                                'effprice': x['effprice'],'carryprice': x['carryprice'],
                                'sprice': x['sprice'],'Date':x['_id']['dt'] } )
    df = pd.DataFrame.from_records(tmp)
    df['Date'] = pd.to_datetime(df.Date,format='%Y%m%d')
    df = df.set_index('Date')
    return df

def rolldates(cts_assigned):
    """
    Converts the date-contract assignment dataframe, coming from which_contract
    into a list of (rolldate,from_contract,to_contract) tuple.    
    """
    tmp = cts_assigned.effcont.dropna().astype(int).diff().dropna()
    rolls = tmp[tmp > 0].index
    cts_assigned_s =cts_assigned.shift(1)
    res = []
    for x in list(rolls):
    	 res.append((x, cts_assigned_s.ix[x].effcont, cts_assigned.ix[x].effcont))
    return res
    
def stitch_contracts(cts_assigned, ctd, price_col):
    """    
    Using a date indexed contracts series and a dictionary of contracts,
    creates a continuous time series. 

    Input
    cts_assigned: Date indexed series with each date mapped to a contract in YYYYMM format
    ctd: Dictionary of contracts, key is a string 'YYYYMM'. This is the universe of contracts for that instrument.
    
    Returns
    Pandas Series
    """

    rolls = rolldates(cts_assigned)
    rolldates2 = []
    for (rolldate, from_con, to_con) in rolls:
    	if str(from_con) in ctd.keys() and str(to_con) in ctd.keys():
	   rolldates2.append((rolldate, from_con, to_con))	   

    rolldates3 = []
    for i,(rolldate, from_con, to_con) in enumerate(rolldates2):
        # it is possible the rollover date is not present in both
        # contracts. This rolldate is calculated arithmetically,
        # remember, so it could fall on a weekend, etc. So we need to
        # seek a date that is in both contracts, starting from the
        # calculated rollover date. The algorithm is go back 0, go
        # forward 1, back 2, so an expanding window of possible dates
        # centered around the first suggestion are all tried. Since
        # the first try is 0, that represents no change i.e. is the
        # first suggestion itself. Whichever date works, the loop will
        # exit immediately and no other tries need to be made.
        for j in range(300):
            rolldate += np.power(-1,j)*datetime.timedelta(days=j)
            if rolldate in ctd[str(from_con)].index and rolldate in ctd[str(to_con)].index:
                break
        assert (j != 299)        
        rolldates3.append((rolldate, from_con, to_con))

    rolldates4 = []; contract_ids = []
    for d,f,t in rolldates3:
    	contract_ids.append(f)
	contract_ids.append(t)
	rolldates4.append(d)

    contracts = [ctd[x].copy() for x in list(np.unique(contract_ids))]
    df_stitched = futures.stitch_prices(contracts, 's', rolldates4, ctd)
    return df_stitched

def which_contract(contract_list, cycle, offset, expday, expmon):
    """
    For a list of contracts it creates a continuous date index, and
    calculates which contract would be effective on that date for a
    given offset (how far ahead) and a rollcycle for the contracts in
    question.

    Returns: A date-indexed Dataframe and an effcont column which points to the
    effective contract for that date.
    """
    assert len(contract_list) > 0
    start_date = contract_list[contract_list.keys()[0]].head(1).index[0] # first dt of first contract
    end_date = contract_list[contract_list.keys()[-1]].tail(1).index[0] # last date of last contract
    delta = end_date - start_date
    dates = []
    # get bizdays between start and end
    for i in range(delta.days + 1):
    	day = start_date + datetime.timedelta(days=i)
	if day.weekday() < 5: dates.append(day)
    df = pd.DataFrame(index=dates)
    
    def closest_biz(d): # get closest biz day
    	diffs = np.abs((d - df.index).days)
    	return df.index[np.argmin(diffs)]

    cycle_d = [futures.contract_month_dict[x] for x in cycle]
    df['effcont'] = np.nan
    for year in np.unique(df.index.year):
    	for c in cycle_d:
	    v = "%d%02d" % (year,c)
	    exp_d = datetime.datetime(year, c, expday)
            # sometimes expiration month is the previous month
            # this happens for crude oil for example
            if expmon=="prev": exp_d = exp_d - datetime.timedelta(days=30)
	    df.loc[closest_biz(exp_d),'effcont'] = v
            
    df = df.fillna(method='bfill')
    # get the contract offset days in the future - the little arithmetic
    # below was necessary to turn offset days into offset business days.
    df['effcont'] = df.effcont.shift(-int(offset*2/3 + 3))

    return df.fillna(method='ffill')

def create_carry(df, offset, contract_list):
    """
    Creates a new column for the carry contract, gets prices for both
    effective and carry contracts.
    
    Input:
    
    df: Dataframe indexed by date which has an 'effcont' column for the effective
    contract for that day
    offset: How far / behind will we look for a carry contract in relation to the
    effective contract.

    Returns:
    Same dataframe df with carry contract, effective price, carry price colunns
    appended.
    """
    df2 = df.copy()
    df2['effcont'] = df2.effcont.astype(str)
    def offset_contract(con):
    	s = pd.to_datetime(con + "15", format='%Y%m%d')
    	ss = s + datetime.timedelta(days=30*offset)
    	return "%d%02d" % (int(ss.year), int(ss.month)) 
    df2['carrycont'] = df2.effcont.map(offset_contract)
    df2['effprice'] = df2.apply(lambda x: contract_list.get(x.effcont).s.get(x.name) if x.effcont in contract_list else np.nan,axis=1)
    df2['carryprice'] = df2.apply(lambda x: contract_list.get(x.carrycont).s.get(x.name) if x.carrycont in contract_list else np.nan,axis=1)
    return df2

def combine_contract_info_save(sym, market, insts, db="findb"):
    """
    Gets all contracts for an instrument, creates carry, stitches them into
    one single time series, and writes all of those to the database as a single record,
    with carry, stitched prices in the same place.

    Inputs
    sym, market: symbol market
    instref: dictionary of all instrument related data for this futures
    """

    connection = MongoClient()
    sticon = connection[db].sticon

    rollcycle = insts[(sym,market)]['rollcycle']
    rolloffset = insts[(sym,market)]['rolloffset']
    expday = insts[(sym,market)]['expday']
    expmon = insts[(sym,market)]['expmon']
    carryoffset = insts[(sym,market)]['carryoffset']
    ctd = get_contracts(market,sym,1990,systemtoday().year)
    cts_assigned = which_contract(ctd, rollcycle, rolloffset, expday, expmon)
    df_carry = create_carry(cts_assigned[pd.isnull(cts_assigned.effcont)==False],int(carryoffset),ctd)
    df_stitched = stitch_contracts(cts_assigned, ctd, 's')
    df_carry['sprice'] = df_stitched

    for srow in df_carry.iterrows():
        dt = int(srow[0].strftime('%Y%m%d'))
        new_row = {"_id": {"sym": sym, "market": market, "dt": dt },
                   "effcont": srow[1].effcont,
                   "carrycont": srow[1].carrycont,
                   "effprice": srow[1].effprice,
                   "carryprice": srow[1].carryprice,
                   "sprice": srow[1].sprice
        }
        #print new_row
        sticon.save(new_row)

def carry_forecast(df, carryoffset):
    vol = util.robust_vol_calc(df.sprice.diff())    
    # we multiply with the sign of the carryoffset below because
    # the offset shows where the carry contract is - if it was
    # -1, meaning we look at the earlier contract, then we need
    # to have carry-price, if ahead then price-carry. The trick
    # with the sign() call below achieves that flip.
    raw_carry = (df.effprice-df.carryprice) / (carryoffset/12.)
    #raw_carry = raw_carry / np.abs(carryoffset/12.)
    forecast = util.carry(raw_carry, vol)
    forecast.loc[forecast > util.MAX_FORECAST] = util.MAX_FORECAST
    forecast.loc[forecast < -util.MAX_FORECAST] = -util.MAX_FORECAST
    return forecast

def ewma(df, fast, slow):
    forecast = util.ewma(df, fast, slow)
    forecast.loc[forecast > util.MAX_FORECAST] = util.MAX_FORECAST
    forecast.loc[forecast < -util.MAX_FORECAST] = -util.MAX_FORECAST
    return forecast

def get_funcs(df, carryoffset):
    return {"carry": lambda : carry_forecast(df, carryoffset),
            "ewmac16_64": lambda : ewma(df.sprice, 16, 64),
            "ewmac32_128": lambda : ewma(df.sprice, 32, 128),
            "ewmac64_256": lambda : ewma(df.sprice, 64, 256) }

def forecast(sym, market, df, dt, insts, conf, calc_sharpe=True):
    df2 = df.copy()
    df2 = df2.ix[df2.index <= dt]
    df2.sprice = df2.sprice / conf['price_divider']["%s_%s" % (sym,market)]
    
    carryoffset = insts[(sym,market)]['carryoffset']
    res = pd.DataFrame()
    funcs = get_funcs(df, carryoffset)
    for x in funcs: res[x] = funcs[x]()
    
    res2 = res * pd.Series(conf['forecast_scalars'])
    res2[res2 < -20.] = -20
    res2[res2 > 20.] = 20    
    res3 = res2 * pd.Series(conf['forecast_weights'])
    res3['forecast'] = res3.sum(axis=1)
    res3['sprice'] = df2.sprice
    
    #res[['carry','ewmac64_256','ewmac32_128','ewmac16_64']].to_csv("out1.csv")
    #res2[['carry','ewmac64_256','ewmac32_128','ewmac16_64']].to_csv("out2.csv")
    #res3[['carry','ewmac64_256','ewmac32_128','ewmac16_64','forecast','sprice']].to_csv("out3.csv")
    #res3.to_csv("out3.csv")

    sharpe = None; tval = None; pval = None
    if calc_sharpe: sharpe,tval,pval = util.sharpe(res3.sprice, res3.forecast)
    return res3.forecast, sharpe, tval, pval

def position_forecast(curr, price, price_vol, notional_trading_capital,
                      percentage_vol_target, point_value, fx_rate, instrument_weight,
                      instrument_div_multiplier, fcast):
    """
    Given recent price, forecast and some other vars, return the position for a
    strategy (instrument) as integer. If '4' is returned that means 4
    contracts. No fractions are possible. If no forecast is passed maximum
    forecast is assumed to maximum long position will be returned. 
    """
    annual_cash_vol_target = notional_trading_capital * (percentage_vol_target/100.)
    daily_vol_target = annual_cash_vol_target / 16
    block_value = price * point_value / 100.
    instrument_ccy_vol = block_value * (price_vol/100.) * 100.
    instrument_value_vol = instrument_ccy_vol * fx_rate
    vol_scalar = daily_vol_target / instrument_value_vol
    sub_position = fcast * vol_scalar / util.LONG_RUN_FCAST
    port_instrument_pos = sub_position * (instrument_weight/100.) * instrument_div_multiplier
    port_instrument_pos = np.round(port_instrument_pos,0)
    return port_instrument_pos

def position_sub(sym, market, df, dt, insts, conf, max_pos = False, calc_sharpe=True): 
    pdiv = conf['price_divider']["%s_%s" % (sym,market)]
    df2 = df.copy()
    df2.sprice = df2.sprice / pdiv
    price = float(df2.sprice.ix[dt])
    vol_window = conf['vol_window']
    vol = pd.rolling_std(df.sprice.dropna().pct_change()*100., window=vol_window)
    price_vol = float(vol.ix[dt])
    fx_rate = conf['exchange'][conf['base_currency']][insts[(sym,market)]['currency']]
    base_currency = conf['base_currency']
    notional_trading_capital = conf['notional_trading_capital']
    percentage_vol_target = conf['percentage_vol_target']
    point_size = insts[(sym,market)]['point_size']
    instrument_weight = conf['instrument_weights']["%s_%s" % (sym,market)]
    instrument_div_multiplier = conf['instrument_div_multiplier']
    fcast = util.MAX_FORECAST; sr = None
    # normally return maximum position, if not max_pos, then
    # calculate forecast and use that
    if not max_pos:
        fcast, sr, tval, pval = forecast(sym, market, df2, dt, insts, conf, calc_sharpe)
        fcast = float(fcast[fcast.index==dt])
    return position_forecast(base_currency, price, price_vol, notional_trading_capital,\
                             percentage_vol_target, point_size, fx_rate, instrument_weight,\
                             instrument_div_multiplier, fcast), sr, tval, pval

def carry_forecast_multiplier(insts):
    res = []
    for (sym, market) in insts.keys():
        df = get_stitched(sym, market)    
        forecast = carry_forecast(df, float(insts[(sym,market)]['carryoffset']))
        res.append(forecast)
    tmp = pd.DataFrame(pd.concat(res))
    tmp = tmp.dropna()
    tmp.columns = ['forecast']
    tmp=tmp.abs().iloc[:,0]
    avg_abs_value=tmp.mean()
    return 10./avg_abs_value 

def portfolio_returns(insts, conf, dt):
    dfs = []; cols = []
    for (sym,market) in insts.keys():
        df = get_stitched(sym, market)
        fc, sharpe, tval, pval = forecast(sym, market, df, dt, insts, conf, calc_sharpe=False)
        res = util.ccy_returns(df.sprice, fc)
        cols.append("%s_%s" % (sym,market))
        dfs.append(res.copy())
    df = pd.concat(dfs,axis=1)
    df.columns = cols
    return df

def sharpe_portfolio(insts, conf, dt):
    df = portfolio_returns(insts, conf, dt)
    w = pd.Series(conf['instrument_weights'])
    df2 = (df * w).sum(axis=1) * conf['instrument_div_multiplier'] / 100.
    mean_return = df2.mean() * 256
    vol = df2.std() * 16
    tval,pval = scipy.stats.ttest_1samp(df2.dropna(), 0)
    print mean_return / vol, tval, pval
