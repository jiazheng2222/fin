from matplotlib.dates import date2num

import pandas as pd
import tushare as ts
import datetime

df = ts.get_hist_data('600036',start='2015-01-05',end='2017-01-09')

print df

quotes = []
for dateStr, item in df.iterrows():
    date_time = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
    dateNum = date2num(date_time)
    open, close, high, low = item[:4]
    tupTmp = (dateNum, open, close, high, low)
    quotes.append(tupTmp)

print quotes
