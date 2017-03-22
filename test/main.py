# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
from matplotlib.dates import WeekdayLocator, DayLocator, DateFormatter, MONDAY
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle

import pandas as pd
import tushare as ts

begin_time = '2015-01-05'
end_time = '2017-01-09'

def _candlestick(ax, quotes, width=0.2, colorup='k', colordown='r',
                 alpha=1.0, ochl=True):
    """
    Plot the time, open, high, low, close as a vertical line ranging
    from low to high.  Use a rectangular bar to represent the
    open-close span.  If close >= open, use colorup to color the bar,
    otherwise use colordown

    Parameters
    ----------
    ax : `Axes`
        an Axes instance to plot to
    quotes : sequence of quote sequences
        data to plot.  time must be in float date format - see date2num
        (time, open, high, low, close, ...) vs
        (time, open, close, high, low, ...)
        set by `ochl`
    width : float
        fraction of a day for the rectangle width
    colorup : color
        the color of the rectangle where close >= open
    colordown : color
         the color of the rectangle where close <  open
    alpha : float
        the rectangle alpha level
    ochl: bool
        argument to select between ochl and ohlc ordering of quotes

    Returns
    -------
    ret : tuple
        returns (lines, patches) where lines is a list of lines
        added and patches is a list of the rectangle patches added
    """

    OFFSET = width / 2.0

    lines = []
    patches = []
    for q in quotes:
        if ochl:
            t, open, close, high, low = q[:5]
        else:
            t, open, high, low, close = q[:5]

        if close >= open:
            color = colorup
            lower = open
            height = close - open
        else:
            color = colordown
            lower = close
            height = open - close

        vline = Line2D(
            xdata=(t, t), ydata=(low, high),
            color=color,
            linewidth=0.5,
            antialiased=True,
        )

        rect = Rectangle(
            xy=(t - OFFSET, lower),
            width=width,
            height=height,
            facecolor=color,
            edgecolor=color,
        )
        rect.set_alpha(alpha)

        lines.append(vline)
        patches.append(rect)
        ax.add_line(vline)
        ax.add_patch(rect)
    ax.autoscale_view()

    return lines, patches

def drawPic(df, code, name):
    mondays = WeekdayLocator(MONDAY)            # 主要刻度
    alldays = DayLocator()                      # 次要刻度
    #weekFormatter = DateFormatter('%b %d')     # 如：Jan 12
    mondayFormatter = DateFormatter('%m-%d-%Y') # 如：2-29-2015
    dayFormatter = DateFormatter('%d')          # 如：12
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(mondayFormatter)

    _candlestick(ax, df, width=0.6, colorup='r', colordown='g')

    ax.xaxis_date()
    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')


    ax.grid(True)
    #plt.title(name + '  ' + code, fontproperties=zhfont)
    plt.show()

def makePicture(code, name):
    df = ts.get_hist_data(code, start=begin_time, end=end_time)
    df = df.sort_index(0)
    drawPic(df, code, name)


makePicture('600036',"test")
