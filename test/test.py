import matplotlib.pyplot as plt

import pandas as pd
import tushare as ts

df = ts.get_hist_data('600036',start='2015-01-05',end='2017-01-09')

print df

with pd.plot_params.use('x_compat', True):
    df.high.plot(color='r',figsize=(10,4),grid='on')
    df.low.plot(color='b',figsize=(10,4),grid='on')

plt.show()
