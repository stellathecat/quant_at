import Quandl, os

fname = '%s/.quandl' % os.environ['HOME']
auth = open(fname).read()

#df = Quandl.get("CME/CLX2004", 
df = Quandl.get("CME/CZ2016", 
                trim_start="2001-01-01",
                trim_end="2020-01-01",
                returns="pandas",
                authtoken=auth)

print df
df.to_csv("out.csv")
