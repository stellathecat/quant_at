
```python
import yaml, strat, sys
sys.path.append('../../data'); import futures
sys.path.append('..'); import util
import pandas as pd

insts = pd.read_csv("futures.csv",index_col=[0,1],comment='#').to_dict('index')
conf = yaml.load(open("futures.yaml", "r"))
```

```python
#sym = 'MP'; market='CME'
#sym = 'ED'; market='CME'
#sym = 'FESX'; market='EUREX'
sym = 'C'; market='CME'
df = futures.get_stitched(sym, market)
#df = df[df.index > '1990-01-01']
#df.to_csv("out-%s.csv" % sym)
dt = '2016-03-10'
print strat.position_sub(sym, market, df, dt, insts, conf, max_pos=False)
#print strat.position_sub(sym, market, df, dt, insts, conf, max_pos=False, calc_sharpe=False)
```

```text
(-12.0, -0.040677566424057156, -0.21402583331015285, 0.83053306987866915)
```


```python
insts = pd.read_csv("futures.csv",index_col=[0,1],comment='#').to_dict('index')
conf = yaml.load(open("futures.yaml", "r"))
dt = '2014-10-15'
#dt = '2014-12-31'
for (sym,market) in insts.keys():
    df = futures.get_stitched(sym, market)
    print sym, market,insts[(sym,market)]['description'], \
          strat.position_sub(sym, market, df, dt, insts, conf, max_pos = True)
```

```text
FESX EUREX Eurostoxx (6.0, None)
FV CME US 5-Year Treasury (6.0, None)
C CME Corn (10.0, None)
ED CME Eurodollar (15.0, None)
MP CME Mexican Peso USD Fx (16.0, None)
FVS EUREX EURO STOXX 50 Volatility (18.0, None)
```

```python
insts = pd.read_csv("futures.csv",index_col=[0,1],comment='#').to_dict('index')
conf = yaml.load(open("futures.yaml", "r"))

dt = '2014-10-15'
for (sym,market) in insts.keys():
    df = futures.get_stitched(sym, market)
    print sym, market,insts[(sym,market)]['description'], \
          strat.position_sub(sym, market, df, dt, insts, conf)
```

```text
FESX EUREX Eurostoxx (0.0, 0.1945316896340981, 0.83520938351813356, 0.40364211849456411)
FV CME US 5-Year Treasury (4.0, 0.7749350086302894, 4.0525215903349352, 5.1216965350649426e-05)
C CME Corn (-6.0, -0.02715330473870922, -0.14286765863136094, 0.88639876325620237)
ED CME Eurodollar (9.0, 0.988083411620042, 5.3801516035428039, 7.6644372766103668e-08)
MP CME Mexican Peso USD Fx (6.0, 0.5332864217295085, 2.4814925899457929, 0.013112769577298832)
FVS EUREX EURO STOXX 50 Volatility (-4.0, 0.2572280283082773, 0.43998636188014656, 0.66007408621959585)
```

```python
dt = '2014-12-01'
for (sym,market) in insts.keys():
    df = futures.get_stitched(sym, market)
    print sym, market,insts[(sym,market)]['description'], \
          strat.position_sub(sym, market, df, dt, insts, conf)
```

```text
FESX EUREX Eurostoxx (1.0, 0.20443050323543163)
FV CME US 5-Year Treasury (6.0, 0.7638639617500368)
C CME Corn (-4.0, -0.03936059297701075)
ED CME Eurodollar (13.0, 0.9799131476319286)
MP CME Mexican Peso USD Fx (4.0, 0.5295086242674839)
FVS EUREX EURO STOXX 50 Volatility (-17.0, 0.3263987348329882)
```
































```python
df = strat.portfolio_returns(insts, conf, dt='2016-01-01')
print len(df)
print len(df.dropna())
print df.corr()
```

```text
7604
749
            FESX_EUREX    FV_CME     C_CME    ED_CME    MP_CME  FVS_EUREX
FESX_EUREX    1.000000  0.055421  0.029401  0.056240  0.070891   0.553598
FV_CME        0.055421  1.000000  0.006311  0.824512 -0.080898  -0.080625
C_CME         0.029401  0.006311  1.000000  0.005564 -0.008140   0.016023
ED_CME        0.056240  0.824512  0.005564  1.000000 -0.063687  -0.057364
MP_CME        0.070891 -0.080898 -0.008140 -0.063687  1.000000   0.165523
FVS_EUREX     0.553598 -0.080625  0.016023 -0.057364  0.165523   1.000000
```

```python
print strat.sharpe_portfolio(insts, conf, dt='2016-01-01')
```

```text
0.79553533976 4.33571321701 1.47161745587e-05
None
```


```python
print strat.carry_forecast_multiplier(insts)
```

```text
19.5757225907
```
