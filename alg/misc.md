
```python
import pandas as pd
f = pd.read_csv("c:/Users/burak/Documents/out-CORN.csv",index_col=0,parse_dates=True)
df = pd.DataFrame(index=f.index)
insts = ['EDOLLAR','US10','EUROSTX','V2X','MXP','CORN']
for c in insts:
    f = pd.read_csv("c:/Users/burak/Documents/out-%s.csv"% c,names=['p'],index_col=0,parse_dates=True)
    df[c] = f['p']
print df.tail(2)
```

```text
                EDOLLAR         US10     EUROSTX          V2X          MXP  \
1981-09-25                                                                   
2016-05-10  -421.468042    -2.958396  460.390369  3368.122983  1647.713180   
2016-05-11  1466.787947  1806.634279 -344.158728 -1397.092227   196.285474   

                   CORN  
1981-09-25               
2016-05-10 -9530.735708  
2016-05-11  2696.234840  
```

```python
w = [0.117,0.117,0.20,0.098,0.233,0.233]
res = (df * w).sum(axis=1) * 1.89 
print res.tail(10)
```

```text
1981-09-25
2016-04-28   -1814.681428
2016-04-29   -1020.466563
2016-05-02   -1928.636754
2016-05-03    3324.714277
2016-05-04     597.012896
2016-05-05    2189.921633
2016-05-06    -971.850633
2016-05-09    4157.028995
2016-05-10   -2767.428751
2016-05-11    1608.769606
dtype: float64
```

```python
import scipy.stats

mean_return = res.mean() * 256
vol = res.std() * 16
tval,pval = scipy.stats.ttest_1samp(res.dropna(), 0)
print mean_return / vol, tval, pval
```

```text
0.492760437735 2.92706154981 0.00343034574536
```


```python
df = futures.get_stitched("ED", "CME")
df.sprice.plot()
plt.savefig('misc_01.png')
print df.head()
```

```text
           carrycont  carryprice effcont  effprice  sprice
Date                                                      
1987-06-18    198806         NaN  198809       NaN   71.76
1987-06-19    198806         NaN  198809       NaN   71.77
1987-06-22    198806         NaN  198809       NaN   71.84
1987-06-23    198806         NaN  198809       NaN   71.84
1987-06-24    198806         NaN  198809       NaN   71.76
```


```python
import util, zipfile, pandas as pd
with zipfile.ZipFile('legacycsv.zip', 'r') as z:
     dftmp = pd.read_csv(z.open('CORN_price.csv'), index_col=0,parse_dates=True )     
dftmp[dftmp.index > '1987-06-01'].PRICE.plot()
plt.savefig('misc_02.png')
```

![](misc_02.png)


```python
raw_carry = df.carryprice-df.effprice
vol = util.robust_vol_calc(df.effprice.diff())
carryoffset = -3
forecast =  util.carry(raw_carry, vol,  carryoffset*1/util.CALENDAR_DAYS_IN_YEAR)
```


```text
0     1
1     2
2     3
3     4
4    10
5    10
dtype: int64
```

