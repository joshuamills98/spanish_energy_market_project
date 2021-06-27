from statsmodels.tsa.stattools import adfuller
import pandas as pd


def adf_test(timeseries, name):
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test for {}:'.format(name))
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic',
                                             'p-value',
                                             '#Lags Used',
                                             'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)
    print(
        'Reject Null Hypothesis, Series is Stationary' if
        dfoutput['Test Statistic'] < dfoutput['Critical Value (1%)'] else
        'Accept Null Hypothesis, Series is Non-Stationary')
    print('\n')
