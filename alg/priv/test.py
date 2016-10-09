import yaml, strat, sys, collections
sys.path.append('../../data')
import futures, datetime
sys.path.append('..'); import util
import numpy as np
import pandas as pd

def test_carry_forecast():
    dt = '1997-10-15'
    sym = "x"; market = "y"

    insts = {}
    insts[(sym,market)] = {'currency': "USD", 'point_size': 1, 'carryoffset': -1}

    conf = {}
    conf['notional_trading_capital'] = 1000000.
    conf['percentage_vol_target'] = 20.0
    conf['vol_window'] = 25
    conf['price_divider'] = {"x_y": 1}
    conf['exchange'] = {'USD': {'EUR': 1.1, 'USD': 1.0} }
    conf['base_currency'] = "USD"
    conf['instrument_weights'] = {'x_y': 100}
    conf['instrument_div_multiplier'] = 1.
    conf['forecast_scalars'] = {"carry": 1.0,"ewmac16_64": 1.0,
                                "ewmac32_128": 1.0,"ewmac64_256": 1.0}
    conf['forecast_weights'] = {"carry": 0.25,"ewmac16_64": 0.25,
                                "ewmac32_128": 0.25,"ewmac64_256": 0.25}
    
    df = create_carry_data(vol=True)
    pos, sr, tval, pval = strat.position_sub(sym, market, df, dt, insts, conf, max_pos=False)
    print pos, sr
    assert sr > 0.5
    assert pos > 100
    
    df = create_carry_data(vol=True,reverse=True)
    pos, sr, tval, pval = strat.position_sub(sym, market, df, dt, insts, conf, max_pos=False)
    print pos, sr
    assert sr > 0.5
    assert pos < -100
    
def create_carry_data(vol = False, reverse=False):
    ctd = collections.OrderedDict()
    for j,y in enumerate(range(1990,1998)):
        # the main rollover contract on the 12th of each year
        # btw years seen above
        start_date = datetime.datetime(y-3, 12, 1)
        end_date = datetime.datetime(y, 12, 31)
        delta = end_date - start_date
        dates = []
        # get bizdays between start and end
        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            if day.weekday() < 5: dates.append(day)
        df = pd.DataFrame(index=dates)
        df['s'] = np.array(range(len(df))) # superfluous value, like 1,2,3
        if vol: df['s'] = df['s'] + 10*np.random.randn(len(df))
        if reverse: df['s'] = 10000 - df['s']
        ctd["%d12" % y] = df
        
        # the carry contract
        start_date = datetime.datetime(y-3, 12, 1)
        end_date = datetime.datetime(y, 11, 30)
        delta = end_date - start_date
        dates = []
        for i in range(delta.days + 1):
            day = start_date + datetime.timedelta(days=i)
            if day.weekday() < 5: dates.append(day)
        df = pd.DataFrame(index=dates)
        df['s'] = 100. +  np.array(range(len(df))) # superfluous value
        if reverse: df['s'] = 10000 - df['s']
        ctd["%d11" % y] = df

    rollcycle = "Z"; rolloffset = 30; expday = 31
    expmon = "curr"; carryoffset = -1

    df_assigned = strat.which_contract(ctd, rollcycle, rolloffset, expday, expmon)
    df_carry = strat.create_carry(df_assigned[pd.isnull(df_assigned.effcont)==False],int(carryoffset),ctd) 
    df_stitched = strat.stitch_contracts(df_assigned, ctd, 's')
    df_carry['sprice'] = df_stitched
    return df_carry
    
def test_carry_stitch():
    df_carry = create_carry_data(True)    
    df_carry = create_carry_data(False)
    assert df_carry.sprice.diff().mean() > 0.9
    assert (df_carry.carryprice - df_carry.effprice).mean() > 0.9
    
if __name__ == "__main__":    
    test_carry_forecast()
    test_carry_stitch()

    
