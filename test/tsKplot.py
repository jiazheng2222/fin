# -*- coding: utf-8 -*-

import  matplotlib.pyplot as plt
from matplotlib.dates import date2num
import datetime

from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import _candlestick

import tushare as ts



def main():
    plt.rcParams['axes.unicode_minus'] = False

    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    mondayFormatter = DateFormatter('%Y-%m-%d')

    df = ts.get_hist_data('600036', start='2015-01-01', end='2015-12-20')
    df = df.sort_index(0)
    quotes = []
    for dateStr, item in df.iterrows():
        date_time = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        dateNum = date2num(date_time)
        open, high, close, low = item[:4]
        tupTmp = (dateNum, open, close, high, low)
        quotes.append(tupTmp)

    if len(quotes) == 0:
        raise SystemExit

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)

    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(mondayFormatter)

    _candlestick(ax, quotes, width=0.6,colorup='r',colordown='g')

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    ax.grid(True)
    plt.title('600036')
    plt.show()
    return

if __name__ == '__main__':
    main()
