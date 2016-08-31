
# Test notebook

```python
from pymongo import MongoClient
import pandas as pd
connection = MongoClient()
db = connection.findb
```

```python
import sys; sys.path.append('..')
import futures
res = futures.get(market="CME", sym="CL", month="F", year=1984, dt=19831205, db="findb")
print res
```

```text
[{u'oi': 5027.0, u'la': nan, u'h': 29.4, u'l': 29.27, u'o': 29.4, u's': 29.3, u'v': 421.0, u'_id': {u'sym': u'CL', u'month': u'F', u'yearmonth': u'1984F', u'year': 1984, u'dt': 19831205, u'market': u'CME'}}]
```


```python
q = {"$query" :{"_id.sym": "GOOGL", "_id.dt": 20160210} }
res = list(db.simple.find(q).limit(1))[0]
print res
```

```text
{u'a': 706.849976, u'c': 706.849976, u'h': 723.219971, u'l': 705.3900150000001, u'o': 711.789978, u'v': 3015700.0, u'_id': {u'dt': 20160210, u'sym': u'GOOGL'}}
```


```python
import sys; sys.path.append('..')
import simple
df = simple.get_multi(['SPY'])
df.SPY.plot()
plt.savefig('mongo_01.png')
```

```python
import simple
df1 = simple.get("AMZN")
df2 = simple.get_multi(['AMZN','GOOGL'])
```

```python
q = {"$query" :{"_id.sym": 'GOOGL'},"$orderby":{"_id.dt" : -1}}
ts = db.simple.find(q).limit(1)
last_date_in_db = int(ts[0]['_id']['dt'])
print last_date_in_db
```

```text
20160511
```

```python
#q = { "$query" : {"_id.sym": "DDD" }, "$orderby": {"_id.dt" : -1} }
q = { "$query" : {"_id.sym": "DDD" } }
#tmp = list(db.simple.find( q ).sort("{$natural:-1}").limit(1))
tmp = list(db.simple.find( q ).sort({"_id.dt":-1}).limit(1))
print tmp
```

```text
[{u'a': 5.08333, u'c': 15.249989999999999, u'h': 15.60999, u'l': 14.67999, 
u'o': 15.06, u'v': 231900.0, u'_id': {u'dt': 20080325, u'sym': u'DDD'}}]
```

```python
print db.simple.count()
db.simple.remove({"_id.sym": "AHP", "_id.dt": 20160205 })
print db.simple.count()
```

```text
14037032
14037032
```

```python
q = {"$query" : {"_id.sym": "CL", "_id.market": "CME", "_id.yearmonth": "2016Z" } }
ts = db.futures.find(q).limit(7)
for t in ts: print t
```

```text
{u'oi': 215671.0, u'la': 48.58, u'h': 48.97, u'l': 46.56, u'o': 47.2, u's': 48.84, u'v': 85063.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160511, u'market': u'CME'}}
{u'oi': 212710.0, u'la': 47.16, u'h': 47.36, u'l': 45.53, u'o': 45.67, u's': 47.28, u'v': 66475.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160510, u'market': u'CME'}}
{u'oi': 208807.0, u'la': 45.67, u'h': 47.94, u'l': 45.63, u'o': 47.4, u's': 45.8, u'v': 78120.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160509, u'market': u'CME'}}
{u'oi': 208912.0, u'la': 46.97, u'h': 47.52, u'l': 45.83, u'o': 46.71, u's': 47.07, u'v': 49713.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160506, u'market': u'CME'}}
{u'oi': 208743.0, u'la': 46.68, u'h': 48.1, u'l': 46.21, u'o': 46.46, u's': 46.55, u'v': 71133.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160505, u'market': u'CME'}}
{u'oi': 207160.0, u'la': 46.44, u'h': 47.22, u'l': 45.7, u'o': 46.45, u's': 46.15, u'v': 69608.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160504, u'market': u'CME'}}
{u'oi': 203387.0, u'la': 46.54, u'h': 47.55, u'l': 45.98, u'o': 47.09, u's': 46.29, u'v': 52203.0, u'_id': {u'sym': u'CL', u'month': u'Z', u'yearmonth': u'2016Z', u'year': 2016, u'dt': 20160503, u'market': u'CME'}}
```

```python
import sys; sys.path.append(".."); import futures
print futures.last_date_in_contract("CL", "CME", "F", 2016, db)
```

```text
20151221
```

```python
ts = list(db.earnings.find( {"_id": 20160211 } ))
print ts
```

```text
[{u'c': [[u'acor', u'Before Market Open'], [u'atvi', u'After Market Close'], [u'iots', u'Time Not Supplied'], [u'ads.de', u'Time Not Supplied'], [u'aap', u'06:30 am ET'], [u'aero', u'Time Not Supplied'], [u'afg.ol', u'Time Not Supplied'], [u'ayr', u'Before Market Open'], [u'alu.pa', u'Time Not Supplied'], [u'alr', u'Before Market Open'], [u'alle', u'Before Market Open'], [u'ab', u'Before Market Open'], [u'alny', u'After Market Close'], [u'aad.de', u'Time Not Supplied'], [u'ambr', u'Time Not Supplied'], [u'aig', u'After Market Close'], [u'apgi', u'Time Not Supplied'], [u'amkr', u'After Market Close'], [u'ahh', u'Before Market Open'], [u'amnf', u'Time Not Supplied'], [u'amnf', u'Time Not Supplied'], [u'ashm.l', u'Before Market Open'], [u'asx.ax', u'Time Not Supplied'], [u'avp', u'Before Market Open'], [u'awdr.ol', u'Before Market Open'], [u'axfo.st', u'Before Market Open'], [u'crg.mi', u'Time Not Supplied'], [u'bar.br', u'01:30 am ET'], [u'bebe', u'After Market Close'], [u'bfg.ax', u'Time Not Supplied'], [u'bng.to', u'After Market Close'], [u'gbf.de', u'01:30 am ET'], [u'binck.as', u'Time Not Supplied'], [u'bcor', u'After Market Close'], [u'nile', u'Before Market Open'], [u'bol.st', u'01:45 am ET'], [u'bwa', u'Before Market Open'], [u'blin', u'Time Not Supplied'], [u'bcov', u'After Market Close'], [u'blmt', u'Time Not Supplied'], [u'bsqr', u'Time Not Supplied'], [u'bts.bk', u'Time Not Supplied'], [u'bg', u'Before Market Open'], [u'bwp.ax', u'Time Not Supplied'], [u'ccg', u'Time Not Supplied'], [u'camt.ta', u'Time Not Supplied'], [u'cf.to', u'After Market Close'], [u'cpla', u'Before Market Open'], [u'cth.l', u'Time Not Supplied'], [u'ctre', u'Time Not Supplied'], [u'cbs', u'After Market Close'], [u'cetx', u'Time Not Supplied'], [u'cetx', u'After Market Close'], [u'cve.to', u'Before Market Open'], [u'kool', u'Time Not Supplied'], [u'cadc', u'Time Not Supplied'], [u'cdi.pa', u'After Market Close'], [u'cix.to', u'Before Market Open'], [u'cty1s.he', u'02:00 am ET'], [u'cst.v', u'Time Not Supplied'], [u'cobz', u'After Market Close'], [u'cce', u'Before Market Open'], [u'coh.ax', u'Time Not Supplied'], [u'cohu', u'After Market Close'], [u'cxp', u'After Market Close'], [u'colm', u'4:00 pm ET'], [u'cdco', u'Time Not Supplied'], [u'cdco', u'Time Not Supplied'], [u'cfms', u'Time Not Supplied'], [u'cor', u'Before Market Open'], [u'cray', u'After Market Close'], [u'cres.ba', u'Time Not Supplied'], [u'cyan', u'Time Not Supplied'], [u'cybr', u'After Market Close'], [u'dva', u'After Market Close'], [u'ddr', u'After Market Close'], [u'dbd', u'Before Market Open'], [u'dno.ol', u'02:00 am ET'], [u'drm.to', u'Time Not Supplied'], [u'dw', u'Before Market Open'], [u'dnb', u'After Market Close'], [u'dysl', u'Time Not Supplied'], [u'edig', u'Time Not Supplied'], [u'elon', u'After Market Close'], [u'eden.pa', u'01:00 am ET'], [u'elli', u'After Market Close'], [u'long', u'Time Not Supplied'], [u'egn', u'After Market Close'], [u'esoa', u'Time Not Supplied'], [u'etm', u'Before Market Open'], [u'esp', u'Time Not Supplied'], [u'eo.pa', u'02:00 am ET'], [u'ffg', u'After Market Close'], [u'feye', u'After Market Close'], [u'faf', u'06:45 am ET'], [u'flir', u'Before Market Open'], [u'fls.co', u'06:00 am ET'], [u'fet', u'After Market Close'], [u'gnca', u'Time Not Supplied'], [u'gxi.de', u'01:30 am ET'], [u'gla1v.he', u'06:00 am ET'], [u'gnc', u'Before Market Open'], [u'gmg.ax', u'Time Not Supplied'], [u'gwo.to', u'Time Not Supplied'], [u'gpi', u'Before Market Open'], [u'grpn', u'After Market Close'], [u'guid', u'After Market Close'], [u'he.to', u'Time Not Supplied'], [u'hdng', u'Time Not Supplied'], [u'he', u'After Market Close'], [u'hgg.l', u'02:00 am ET'], [u'hex.ol', u'01:00 am ET'], [u'huh1v.he', u'01:30 am ET'], [u'hun', u'Before Market Open'], [u'ipwr', u'Time Not Supplied'], [u'nk.pa', u'After Market Close'], [u'imsc', u'Time Not Supplied'], [u'incy', u'07:00 am ET'], [u'iag.to', u'Before Market Open'], [u'infn', u'After Market Close'], [u'inf.l', u'Before Market Open'], [u'ifp.to', u'Time Not Supplied'], [u'ivc', u'Before Market Open'], [u'irsa.ba', u'Before Market Open'], [u'iti', u'Time Not Supplied'], [u'iwg.v', u'Time Not Supplied'], [u'kat.to', u'Time Not Supplied'], [u'060250.kq', u'Time Not Supplied'], [u'k', u'Before Market Open'], [u'king', u'After Market Close'], [u'kkr', u'Before Market Open'], [u'knl', u'After Market Close'], [u'kn', u'After Market Close'], [u'kog.ol', u'Time Not Supplied'], [u'or.pa', u'After Market Close'], [u'lr.pa', u'01:30 am ET'], [u'lc', u'Before Market Open'], [u'liox', u'Time Not Supplied'], [u'logm', u'After Market Close'], [u'lpx', u'Before Market Open'], [u'lpla', u'After Market Close'], [u'lpn.bk', u'Time Not Supplied'], [u'lxft', u'After Market Close'], [u'manu', u'Before Market Open'], [u'mfc.to', u'Before Market Open'], [u'mdf.to', u'Time Not Supplied'], [u'merc', u'After Market Close'], [u'msl.to', u'Time Not Supplied'], [u'meo.de', u'01:30 am ET'], [u'mgr.ax', u'Time Not Supplied'], [u'mztf.ta', u'Time Not Supplied'], [u'tap', u'Before Market Open'], [u'mgi', u'Before Market Open'], [u'type', u'Before Market Open'], [u'mww', u'Before Market Open'], [u'mos', u'Before Market Open'], [u'mpsx', u'After Market Close'], [u'nnn', u'Before Market Open'], [u'nci', u'Before Market Open'], [u'ntwk', u'Before Market Open'], [u'nbix', u'After Market Close'], [u'nr', u'After Market Close'], [u'nice.ta', u'Before Market Open'], [u'nlsn', u'Before Market Open'], [u'nokia.he', u'01:00 am ET'], [u'northm.co', u'Time Not Supplied'], [u'nwe', u'Before Market Open'], [u'nas.ol', u'01:00 am ET'], [u'npro.ol', u'01:00 am ET'], [u'nus', u'After Market Close'], [u'nuva', u'After Market Close'], [u'ozm', u'Before Market Open'], [u'ork.ol', u'01:00 am ET'], [u'out1v.he', u'02:00 am ET'], [u'p', u'After Market Close'], [u'phm.v', u'Time Not Supplied'], [u'pbf', u'Before Market Open'], [u'pbfx', u'Before Market Open'], [u'pdfs', u'After Market Close'], [u'btu', u'Before Market Open'], [u'pag', u'Before Market Open'], [u'pep', u'Before Market Open'], [u'ri.pa', u'01:30 am ET'], [u'pnk', u'Before Market Open'], [u'pjt', u'Before Market Open'], [u'pkc1v.he', u'01:15 am ET'], [u'ptsx', u'Time Not Supplied'], [u'pd.to', u'Before Market Open'], [u'pdex', u'Time Not Supplied'], [u'pub.pa', u'Before Market Open'], [u'qlik', u'After Market Close'], [u'q', u'Before Market Open'], [u'quot', u'After Market Close'], [u'rmr1v.he', u'02:00 am ET'], [u'rec.mi', u'Time Not Supplied'], [u'rsg', u'After Market Close'], [u'rxl.pa', u'01:30 am ET'], [u'rai', u'Before Market Open'], [u'rio.l', u'Before Market Open'], [u'rcky', u'Time Not Supplied'], [u'rovi', u'After Market Close'], [u'sanw', u'Time Not Supplied'], [u'saja', u'Time Not Supplied'], [u'ssn.ax', u'Time Not Supplied'], [u'scss', u'After Market Close'], [u'semc.st', u'Time Not Supplied'], [u'shp.l', u'Time Not Supplied'], [u'5cp.si', u'Time Not Supplied'], [u'szmk', u'Time Not Supplied'], [u'sma.to', u'After Market Close'], [u'gle.pa', u'01:00 am ET'], [u'local.pa', u'Before Market Open'], [u'sofo', u'Time Not Supplied'], [u'son', u'Before Market Open'], [u'spdc', u'Time Not Supplied'], [u'sqd.v', u'Time Not Supplied'], [u'ssnc', u'After Market Close'], [u'stc', u'06:15 am ET'], [u'sum', u'Before Market Open'], [u'sun.ax', u'Time Not Supplied'], [u'syz.v', u'Time Not Supplied'], [u'syn.v', u'Time Not Supplied'], [u'symx', u'After Market Close'], [u'tbl.to', u'Time Not Supplied'], [u't.to', u'Before Market Open'], [u'teri3.sa', u'Time Not Supplied'], [u'teva.ta', u'07:00 am ET'], [u'tgh', u'09:00 am ET'], [u'tri.to', u'Before Market Open'], [u'time', u'Before Market Open'], [u'tmd.to', u'Time Not Supplied'], [u'x.to', u'After Market Close'], [u'top.co', u'06:00 am ET'], [u'fp.pa', u'02:00 am ET'], [u'towr', u'Time Not Supplied'], [u'rnw.to', u'Time Not Supplied'], [u'trp.to', u'Before Market Open'], [u'tfi.to', u'After Market Close'], [u'tcl.ax', u'Time Not Supplied'], [u'tzoo', u'Before Market Open'], [u'ths', u'Before Market Open'], [u'trip', u'Time Not Supplied'], [u'trup', u'After Market Close'], [u'tssi', u'Before Market Open'], [u'ttkom.is', u'After Market Close'], [u'vakbn.is', u'Time Not Supplied'], [u'ulbi', u'Before Market Open'], [u'uns.to', u'Time Not Supplied'], [u'unitech.ns', u'Time Not Supplied'], [u'vrns', u'After Market Close'], [u'woof', u'08:00 am ET'], [u'vcm.to', u'Time Not Supplied'], [u'vei.ol', u'01:00 am ET'], [u'vrsn', u'After Market Close'], [u'vah.ax', u'Time Not Supplied'], [u'vsto', u'Before Market Open'], [u'vcra', u'Time Not Supplied'], [u'vg', u'Before Market Open'], [u'gra', u'06:00 am ET'], [u'wbc', u'Before Market Open'], [u'wso', u'Before Market Open'], [u'web', u'After Market Close'], [u'wft.to', u'After Market Close'], [u'wwav', u'Before Market Open'], [u'int', u'Before Market Open'], [u'wwe', u'Before Market Open'], [u'wynn', u'After Market Close'], [u'xplr', u'Time Not Supplied'], [u'yoo.v', u'Time Not Supplied'], [u'yar.ol', u'02:00 am ET'], [u'y.to', u'Time Not Supplied'], [u'zg', u'After Market Close'], [u'zurn.vx', u'12:45 am ET']], u'_id': 20160211}]
```

```python
print db.earnings.count()
db.earnings.remove({"_id": 20160210 })
print db.earnings.count()
```

```text
2635
2635
```

```python
import simple
from pymongo import MongoClient
import pandas as pd
connection = MongoClient()
db = connection.findb
dt = 20160517
res = simple.get_hft("IBB", dt)
res['m']  = (res['high'].astype(float) + res['low'].astype(float)) / 2.
print res.m.mean(), res.m.std(), res.m.min(), res.m.max()
q = {"$query" :{"_id.sym": "IBB", "_id.dt": dt} }
res = list(db.simple.find(q).limit(1))[0]
print res
```

```text
260.334341139 1.09759745098 258.455 262.555
{u'a': 259.170013, u'c': 259.170013, u'h': 262.859985, u'l': 258.140015, u'o': 261.459991, u'hft': {u'220415': {u'high': u'258.9000', u'close': u'258.7100', u'open': u'258.7500', u'low': u'258.5300', u'volume': u'9000'}, u'182907': {u'high': u'262.3100', u'close': u'261.6400', u'open': u'262.1200', u'low': u'261.6400', u'volume': u'15400'}, u'165905': {u'high': u'261.7050', u'close': u'260.7800', u'open': u'261.4200', u'low': u'260.6900', u'volume': u'24100'}, u'172413': {u'high': u'261.3200', u'close': u'260.8490', u'open': u'260.8700', u'low': u'260.2750', u'volume': u'26300'}, u'170403': {u'high': u'260.9355', u'close': u'260.1800', u'open': u'260.7500', u'low': u'260.0500', u'volume': u'37400'}, u'221951': {u'high': u'259.2200', u'close': u'258.9150', u'open': u'259.1100', u'low': u'258.9000', u'volume': u'20800'}, u'163455': {u'high': u'261.5000', u'close': u'261.3000', u'open': u'261.2300', u'low': u'260.0600', u'volume': u'0'}, u'214414': {u'high': u'258.7100', u'close': u'258.5800', u'open': u'258.5800', u'low': u'258.3000', u'volume': u'13700'}, u'180439': {u'high': u'261.1900', u'close': u'260.9000', u'open': u'261.1400', u'low': u'260.8500', u'volume': u'6800'}, u'220903': {u'high': u'259.3600', u'close': u'259.2100', u'open': u'258.7100', u'low': u'258.6900', u'volume': u'8000'}, u'180923': {u'high': u'261.1050', u'close': u'261.0000', u'open': u'260.8100', u'low': u'260.8000', u'volume': u'3600'}, u'230000': {u'high': u'259.7400', u'close': u'259.7400', u'open': u'259.7400', u'low': u'259.7400', u'volume': u'700'}, u'195904': {u'high': u'260.3400', u'close': u'260.2800', u'open': u'260.3300', u'low': u'259.9235', u'volume': u'7000'}, u'195417': {u'high': u'260.5900', u'close': u'260.4266', u'open': u'260.4999', u'low': u'260.1000', u'volume': u'7000'}, u'191937': {u'high': u'261.3200', u'close': u'261.0300', u'open': u'261.1700', u'low': u'260.9000', u'volume': u'19600'}, u'201918': {u'high': u'260.0300', u'close': u'259.7700', u'open': u'260.0300', u'low': u'259.5600', u'volume': u'9200'}, u'181953': {u'high': u'261.8400', u'close': u'261.6600', u'open': u'261.0080', u'low': u'260.9600', u'volume': u'5100'}, u'181327': {u'high': u'261.2400', u'close': u'260.6228', u'open': u'261.1600', u'low': u'260.6228', u'volume': u'4600'}, u'172951': {u'high': u'260.7200', u'close': u'260.5600', u'open': u'260.4825', u'low': u'260.1700', u'volume': u'18400'}, u'213901': {u'high': u'258.8600', u'close': u'258.4811', u'open': u'258.6200', u'low': u'258.4000', u'volume': u'11300'}, u'175430': {u'high': u'261.2200', u'close': u'261.2200', u'open': u'260.6600', u'low': u'260.6600', u'volume': u'3800'}, u'192936': {u'high': u'260.9400', u'close': u'260.7200', u'open': u'260.6100', u'low': u'260.5600', u'volume': u'6800'}, u'173413': {u'high': u'260.4125', u'close': u'260.4125', u'open': u'260.2500', u'low': u'259.7350', u'volume': u'22000'}, u'203917': {u'high': u'260.4400', u'close': u'260.0000', u'open': u'260.3700', u'low': u'260.0000', u'volume': u'7900'}, u'185410': {u'high': u'262.8578', u'close': u'262.1540', u'open': u'262.5900', u'low': u'262.1540', u'volume': u'14100'}, u'200441': {u'high': u'260.3450', u'close': u'259.7800', u'open': u'260.2000', u'low': u'259.7200', u'volume': u'10800'}, u'210432': {u'high': u'260.3600', u'close': u'260.2100', u'open': u'260.1700', u'low': u'259.9101', u'volume': u'8500'}, u'184925': {u'high': u'262.6700', u'close': u'262.5900', u'open': u'262.5100', u'low': u'262.3400', u'volume': u'7500'}, u'223958': {u'high': u'259.0800', u'close': u'259.0700', u'open': u'258.8800', u'low': u'258.7950', u'volume': u'19500'}, u'190411': {u'high': u'262.0200', u'close': u'261.7500', u'open': u'261.8200', u'low': u'261.7500', u'volume': u'16800'}, u'191455': {u'high': u'261.6400', u'close': u'261.2300', u'open': u'261.6400', u'low': u'261.1890', u'volume': u'3700'}, u'212459': {u'high': u'259.4700', u'close': u'258.9100', u'open': u'259.3400', u'low': u'258.9100', u'volume': u'9600'}, u'211905': {u'high': u'259.9700', u'close': u'259.3400', u'open': u'259.7800', u'low': u'259.2800', u'volume': u'8800'}, u'222902': {u'high': u'258.9400', u'close': u'258.6400', u'open': u'258.9400', u'low': u'258.3600', u'volume': u'14900'}, u'184300': {u'high': u'262.7900', u'close': u'262.5016', u'open': u'262.5500', u'low': u'262.3200', u'volume': u'6600'}, u'164421': {u'high': u'261.4000', u'close': u'260.2000', u'open': u'260.1800', u'low': u'260.1200', u'volume': u'25000'}, u'193911': {u'high': u'261.4946', u'close': u'261.4946', u'open': u'260.8950', u'low': u'260.8200', u'volume': u'3800'}, u'210913': {u'high': u'260.2600', u'close': u'259.8600', u'open': u'260.2514', u'low': u'259.8300', u'volume': u'10200'}, u'204253': {u'high': u'260.3700', u'close': u'260.1400', u'open': u'260.1100', u'low': u'260.1100', u'volume': u'3900'}, u'222457': {u'high': u'259.0000', u'close': u'258.9300', u'open': u'258.7900', u'low': u'258.7000', u'volume': u'10800'}, u'171919': {u'high': u'260.9400', u'close': u'260.9150', u'open': u'260.1750', u'low': u'260.0000', u'volume': u'22100'}, u'215441': {u'high': u'258.6100', u'close': u'258.5100', u'open': u'258.3000', u'low': u'258.3000', u'volume': u'6400'}, u'225400': {u'high': u'259.3200', u'close': u'259.3000', u'open': u'259.1700', u'low': u'258.9100', u'volume': u'26100'}, u'202833': {u'high': u'260.0000', u'close': u'260.0000', u'open': u'259.8500', u'low': u'259.7200', u'volume': u'4000'}, u'204915': {u'high': u'260.8700', u'close': u'260.6700', u'open': u'260.3300', u'low': u'260.3300', u'volume': u'23400'}, u'200905': {u'high': u'260.0800', u'close': u'259.9300', u'open': u'259.8500', u'low': u'259.8500', u'volume': u'6000'}, u'205936': {u'high': u'261.0800', u'close': u'260.2750', u'open': u'261.0000', u'low': u'260.1400', u'volume': u'37000'}, u'225959': {u'high': u'259.3300', u'close': u'259.3000', u'open': u'259.3200', u'low': u'258.8700', u'volume': u'60800'}, u'173958': {u'high': u'261.1000', u'close': u'261.0000', u'open': u'260.3100', u'low': u'260.3000', u'volume': u'14800'}, u'183957': {u'high': u'262.5700', u'close': u'262.5700', u'open': u'262.0100', u'low': u'262.0100', u'volume': u'5300'}, u'170908': {u'high': u'260.9900', u'close': u'260.4950', u'open': u'260.2150', u'low': u'260.0100', u'volume': u'42600'}, u'224903': {u'high': u'259.4600', u'close': u'259.3500', u'open': u'259.0275', u'low': u'258.8500', u'volume': u'26200'}, u'192405': {u'high': u'261.0900', u'close': u'260.6825', u'open': u'260.9350', u'low': u'260.6100', u'volume': u'15400'}, u'205459': {u'high': u'260.8500', u'close': u'260.8500', u'open': u'260.6600', u'low': u'260.5400', u'volume': u'31800'}, u'174939': {u'high': u'261.3800', u'close': u'260.6703', u'open': u'261.1000', u'low': u'260.6703', u'volume': u'7500'}, u'213444': {u'high': u'258.8000', u'close': u'258.5407', u'open': u'258.7900', u'low': u'258.2900', u'volume': u'10600'}, u'182428': {u'high': u'262.0000', u'close': u'262.0000', u'open': u'261.6700', u'low': u'261.5400', u'volume': u'5600'}, u'214933': {u'high': u'258.9500', u'close': u'258.4970', u'open': u'258.6400', u'low': u'258.4700', u'volume': u'8900'}, u'221400': {u'high': u'259.3400', u'close': u'259.1100', u'open': u'259.0000', u'low': u'258.9300', u'volume': u'11800'}, u'215903': {u'high': u'258.8400', u'close': u'258.6850', u'open': u'258.2950', u'low': u'258.1400', u'volume': u'10100'}, u'163955': {u'high': u'262.0700', u'close': u'260.9400', u'open': u'261.3000', u'low': u'260.4500', u'volume': u'55800'}, u'201412': {u'high': u'260.1200', u'close': u'260.1200', u'open': u'259.8101', u'low': u'259.8101', u'volume': u'3900'}, u'175941': {u'high': u'261.4500', u'close': u'261.1000', u'open': u'261.3700', u'low': u'261.0900', u'volume': u'5900'}, u'193405': {u'high': u'260.9700', u'close': u'260.8883', u'open': u'260.7983', u'low': u'260.5000', u'volume': u'5200'}, u'190917': {u'high': u'261.8600', u'close': u'261.5600', u'open': u'261.8600', u'low': u'261.4600', u'volume': u'6300'}, u'165406': {u'high': u'262.8600', u'close': u'261.3100', u'open': u'261.6500', u'low': u'261.3100', u'volume': u'61800'}, u'194443': {u'high': u'261.5600', u'close': u'260.7899', u'open': u'261.5599', u'low': u'260.6200', u'volume': u'9400'}, u'185911': {u'high': u'262.2200', u'close': u'261.8200', u'open': u'262.1500', u'low': u'261.5901', u'volume': u'13500'}, u'212905': {u'high': u'259.0500', u'close': u'258.9600', u'open': u'258.8900', u'low': u'258.6500', u'volume': u'22100'}, u'211428': {u'high': u'259.9100', u'close': u'259.8600', u'open': u'259.9100', u'low': u'259.5000', u'volume': u'19300'}, u'174445': {u'high': u'261.1400', u'close': u'261.1400', u'open': u'260.8300', u'low': u'260.6500', u'volume': u'10600'}, u'202406': {u'high': u'259.9106', u'close': u'259.8500', u'open': u'259.9106', u'low': u'259.6950', u'volume': u'6800'}, u'183416': {u'high': u'262.0500', u'close': u'261.8600', u'open': u'261.6300', u'low': u'261.5000', u'volume': u'9700'}, u'203425': {u'high': u'260.4700', u'close': u'260.3660', u'open': u'260.0250', u'low': u'260.0250', u'volume': u'6300'}, u'164955': {u'high': u'261.7600', u'close': u'261.7400', u'open': u'260.3400', u'low': u'260.1100', u'volume': u'30300'}, u'171415': {u'high': u'260.6800', u'close': u'260.2761', u'open': u'260.5000', u'low': u'260.0700', u'volume': u'34900'}, u'224458': {u'high': u'259.2500', u'close': u'259.0150', u'open': u'259.1250', u'low': u'258.6900', u'volume': u'19800'}, u'194907': {u'high': u'260.7000', u'close': u'260.4200', u'open': u'260.7000', u'low': u'260.3300', u'volume': u'7500'}, u'223459': {u'high': u'258.9950', u'close': u'258.8000', u'open': u'258.7450', u'low': u'258.6300', u'volume': u'11100'}}, u'v': 1405800.0, u'_id': {u'dt': 20160517, u'sym': u'IBB'}}
```
























