import os, futures, pandas as pd, datetime, simple
from pymongo import MongoClient
import numpy as np, sys, Quandl
sys.path.append('../alg')
import util, collections, futures2
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

testdb = "fakedb"

def load_data(contract,subdir,start,end):
    f = contract.replace("/","-")
    f = "./test/%s/%s.csv" % (subdir,f)
    if not os.path.isfile(f): raise Quandl.Quandl.DatasetNotFound()
    df = pd.read_csv(f)
    df = df.set_index("Date")
    df = df[df.index > start]
    return df
    
def fake_download_1(contract,start,end):
    return load_data(contract, "data_1",start,end)

def fake_download_2(contract,start,end):
    return load_data(contract, "data_2",start,end)

def fake_download_3(contract,start,end):
    return load_data(contract, "data_3",start,end)


def fake_today_1():
    return datetime.datetime(2016, 5, 1) 

def fake_today_2():
    return datetime.datetime(1984, 1, 1) 

def fake_today_726():
    return datetime.datetime(1983, 7, 26) 

def fake_today_727():
    return datetime.datetime(1983, 7, 27) 

def init():
    c = MongoClient()
    c[testdb].futures.drop()
    c[testdb].tickers.drop()
    return c[testdb]

def test_simple():
    db = init()
    futures.download_data(downloader=fake_download_1,
                          today=fake_today_1,
                          db=testdb,
                          years=(1984,1985),
                          fin="futures.csv")
    res = futures.get(market="CME", sym="CL", month="F", year=1984, dt=19831205, db=testdb)
    assert (res[0]['oi'] == 5027.0)
    res = futures.get(market="CME", sym="CL", month="G", year=1984, dt=19830624, db=testdb)
    assert (res[0]['oi'] == 5.0)
    res = futures.last_contract("CL","CME", db)
    assert (res[0]['_id']['month'] == 'G')
    res = futures.existing_nonexpired_contracts("CL","CME", fake_today_1(), db)
    assert (len(res) == 0)
    res = futures.existing_nonexpired_contracts("CL","CME", fake_today_2(), db)
    assert (len(res) > 0)
    res = futures.get_contract(market="CME", sym="CL", month="G", year=1984, db=testdb)
    assert (len(res)==143)
    
def test_incremental():
    db = init()
    futures.download_data(downloader=fake_download_2,today=fake_today_726,
                          db=testdb, years=(1984,1985))
    print futures.last_date_in_contract("CL","CME","F", 1984, db)
    assert (futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830726)
    futures.download_data(downloader=fake_download_3,today=fake_today_727,
                          db=testdb, years=(1984,1985))
    assert (futures.last_date_in_contract("CL","CME","F", 1984, db) == 19830727)

def test_stitch():
    stitch_points = ['2015-03-13','2015-04-15']
    dfs = []; ctd = {}
    base = 'test/data_stitch/vix%s.csv'
    for f in ['may','june','july']:
        tmp = pd.read_csv(base % f,index_col=0,parse_dates=True)
        dfs.append(tmp); ctd[f] = tmp
    res = futures.stitch_prices(dfs,'Settle',stitch_points, ctd)
    exp = pd.read_csv('test/data_stitch/stitch_expected.csv',index_col=0,parse_dates=True)
    exp['res'] = res
    assert (np.sum(exp.res-exp.Settle) < 1)

def test_missing_contract():
    db = init()
    futures.download_data(downloader=fake_download_1,today=fake_today_1,
                          db=testdb, years=(1984,1985))
    res = futures.get_contract(market="CME", sym="CL", month="Z", year=1984, db=testdb)
    assert (res==None)
    
def test_one_load():
    db = init()
    futures.download_and_save(work_items=[('CME','CL','G',1984,'1980-01-01')],
                              db=db.futures,
                              downloader=fake_download_2)
    
    res = futures.get_contract(market="CME", sym="CL", month="G", year=1984, db=testdb)
    assert (len(res) == 22)

def test_returns_sharpe_skew():
    import util, zipfile, pandas as pd
    with zipfile.ZipFile('../alg/legacycsv.zip', 'r') as z:
         df = pd.read_csv(z.open('EDOLLAR_price.csv'), index_col=0,parse_dates=True )

    fast_ewma = pd.ewma(df.PRICE, span=32)
    slow_ewma = pd.ewma(df.PRICE, span=128)
    raw_ewmac = fast_ewma - slow_ewma
    vol = util.robust_vol_calc(df.PRICE.diff())
    forecast = raw_ewmac /  vol
    sr,tval,pval = util.sharpe(df.PRICE, forecast)
    assert sr-0.50 < 0.01
    s = util.skew(df.PRICE, forecast)
    assert s-(-0.57) < 0.01

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

    df_assigned = futures2.which_contract(ctd, rollcycle, rolloffset, expday, expmon)
    df_carry = futures2.create_carry(df_assigned[pd.isnull(df_assigned.effcont)==False],int(carryoffset),ctd) 
    df_stitched = futures2.stitch_contracts(df_assigned, ctd, 's')
    df_carry['sprice'] = df_stitched
    return df_carry
    
def test_carry_stitch():
    if not os.path.isfile("futures2.py"):
        print 'futures2.py not there.. skipping'
        return
    df_carry = create_carry_data(True)    
    df_carry = create_carry_data(False)
    assert df_carry.sprice.diff().mean() > 0.9
    assert (df_carry.carryprice - df_carry.effprice).mean() > 0.9

if __name__ == "__main__":    
    simple.check_mongo()    
    test_simple()
    test_incremental()
    test_stitch()
    test_missing_contract()
    test_one_load()
    test_returns_sharpe_skew()
    test_carry_stitch()
