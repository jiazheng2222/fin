import  matplotlib.pyplot as plt

from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY, YEARLY
from matplotlib.finance import _quotes_historical_yahoo, _candlestick

def main():
    plt.rcParams['axes.unicode_minus'] = False
    ticker = '600028'
    ticker += '.ss'

    date1 = (2015,8,1)
    date2 = (2016,1,1)

    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    mondayFormatter = DateFormatter('%Y-%m-%d')
    mondayFormatter = DateFormatter('%d')

    quotes = _quotes_historical_yahoo(ticker, date1, date2)

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
    plt.title('600028')
    plt.show()
    return

if __name__ == '__main__':
    main()
