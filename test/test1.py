# -*- coding: utf-8 -*-

import datetime
from matplotlib import finance, mlab
import numpy as np
import matplotlib.pyplot as plt

def load_data(code, start_date, end_date):
    fh = finance.fetch_historical_yahoo(code, start_date, end_date)
    data = mlab.csv2rec(fh)
    fh.close()
    data.sort()
    return data

def show_data(data):
    close_data = data['close']
    date_data = data['date']
    #plt.autoscale(True, 'both', None)
    plt.rc('axes', grid=True)
    plt.rc('grid', color='0.75', linestyle='-', linewidth=0.5)
    plt.plot(date_data, close_data)
    plt.xlabel('Date')
    plt.ylabel('Close')
    plt.setp(plt.gca().get_xticklabels(), rotation=20, horizontalalignment='right')
    plt.show()


show_data (load_data('600036.ss', (2012,01,01),(2015,01,01)))
