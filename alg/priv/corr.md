
```python
import yaml, strat, sys
sys.path.append('../../data'); import futures
sys.path.append('..'); import util
import pandas as pd

insts = pd.read_csv("futures.csv",index_col=[0,1],comment='#').to_dict('index')
conf = yaml.load(open("futures.yaml", "r"))
```



```python
import pandas as pd
dfs = []
insts = ['EDOLLAR','US10','EUROSTX','V2X','MXP','CORN']
for c in insts:
    df = pd.read_csv("c:/Users/burak/Documents/kod/books/Systematic_Trading/pysystemtrade/examples/out-%s.csv" % c,index_col=0,parse_dates=True)
    dfs.append(df)
df = pd.concat(dfs,axis=1)
df.columns = insts
pandl=df.cumsum().resample("W").diff()
print pandl.corr()
```

```text
          EDOLLAR      US10   EUROSTX       V2X       MXP      CORN
EDOLLAR  1.000000  0.832953 -0.011834 -0.021787 -0.110608 -0.008152
US10     0.832953  1.000000 -0.052660 -0.070974 -0.137588  0.013764
EUROSTX -0.011834 -0.052660  1.000000  0.573119  0.016384  0.008217
V2X     -0.021787 -0.070974  0.573119  1.000000  0.223882  0.073453
MXP     -0.110608 -0.137588  0.016384  0.223882  1.000000 -0.006415
CORN    -0.008152  0.013764  0.008217  0.073453 -0.006415  1.000000
```


