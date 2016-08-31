# INTRODUCTION

This folder will contain a Python / MongoDB based database /
downloader for financial data. It will do this from the open sources,
be able to update itself incrementally.

## Requirements

`conda install` or `pip install`

* pandas
* scipy
* numpy
* pymongo 3.x 
* quandl

## Data

Symbols are retrieved from seperate csv files under `data`
folder. [Details](data/README.md).

* simple.csv: Stock, ETF data.
* futures.csv: Commodity Futures.
* hft.csv: High-frequency data in 5-minute bars.
* earnings.csv: List of companies announcing their earnings per day.

Composite unique Id for a simple finance record is comprised of the
symbol `sym` and the date `dt`.

Futures data is retrieved from Quandl; we use their API access, for
which you need to create a `.quandl` file with the API access key in
it (no newlines) under your home directory.

## Usage

Simplest usage for mass download is `python simple.py` (start your
Mongo instance first of course). This will read all symbols from under
`data/simple.csv` and start downloading them. Same for `python
futures.py`.

For parallel execution, we provided a chunking ability [works for
simple, TBD for futures],

```
python simple.py 0 4
```

This divides the symbol list into 4 chunks, and processes the 0th one
(it could have been 1, 2, etc). For parallel execution 4 processes of
`simple.py` would be started, each for / using a different chunk
number.  These processes would ideally be run under a monitoring tool,
we prefer [dand][1]. A sample configuration for this tool can be found
in [dand.conf](dand.conf) which can simply be executed with `python
dand.py dand.conf`.

Parallel inserts into Mongo are no problem, both in terms of
scalability and collisions; key value stores are particularly good at
parallel inserts, and since we are dividing the symbol list
before handing it over to a processor, no two processes can insert or
update on the same unique id. 

For futures

```
python futures.py
```

For research, data exploration purposes, there are utility
functions. To see all data for symbol DIJA,

```
import simple
df = simple.get("DJIA")
```

For multiple symbols in one Dataframe,

```
df = simple.get_multi(['DJIA','GOOG'])
```

A simple query from mongo shell to see all futures

```
use futures
db.futures.count()
```

Show a certain amount of futures

```
db.futures.find().limit(10)
```

Show all records for a symbol and market

```
db.futures.find({"_id.sym": "CL", "_id.market": "CME"})
db.futures.find({"_id.sym": "CL", "_id.market": "CME"}).sort({ "_id.month": 1 })
```

To see all earnings announcements for a particular date, 

```
db.earnings.find( {"_id": 20110126 } )
```

which gives all companies announcing their earnings as a list of
tuples for January 26, 2011.

For symbols for which we have high-frequency data available, minute level tick
data for a symbol and specific day can be accessed with,

```
df = simple.get_hft("AHP", 20160213)
```

## Indexing

In the case of composite Ids, indexes might not be created properly in
MongoDB. Show indexes (on mongoshell)

```
db.futures.getIndexes()
```

A simple index

```
db.futures.createIndex("_id")
```

For a number of selected columns (actually the one below is mandatory
for futures.py and the second one for simple.py)

```
db.futures.createIndex( { "_id.sym": 1, "_id.market": 1, "_id.month": -1, "_id.year": -1, "_id.dt": -1 } )
db.futures.createIndex( { "_id.sym": 1, "_id.market": 1, "_id.yearmonth": -1} )
db.futures.createIndex( { "_id.sym": 1, "_id.dt": -1 } )
```

To check indexing is working properly

```
db.futures.find( {"_id.sym": "AMZN", "_id.dt": 20070101 } ).limit(1).explain()
```

This should say something about BTrees, and indicate the table is not
fully scanned, if the index is not there.

Drop database

```
use findb
db.dropDatabase()
```

[1]: https://github.com/burakbayramli/kod/tree/master/dand

[2]: https://www.stlouisfed.org

