
# Test 

```python
import sys; sys.path.append('..')
import simple
df = simple.get_multi(['XME','DBA','IBB'])
fig, axes = plt.subplots(nrows=3, ncols=1)
df.XME.plot(ax=axes[0],title='XME')
df.DBA.plot(ax=axes[1],title='DBA')
df.IBB.plot(ax=axes[2],title='IBB')
plt.subplots_adjust(hspace=2.0)
plt.savefig('nb1_01.png')
```

```python
import sys; sys.path.append('../../book')
import corr
print corr.p_corr(df.DBA,df.IBB)
print corr.p_corr(df.XME,df.DBA)
```

```text
(-0.51755969651186839, -29.347357044897883, 0.0)
(0.83024084749635096, 74.309754051931009, 0.0)
```






















