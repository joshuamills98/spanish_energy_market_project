from statsmodels.tsa.stattools import adfuller
from scipy.stats import normaltest
import pandas as pd
import os


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


def normal_test(timeseries, name, alpha=5e-3):
    print('Results of D’Agostino and Pearson Test for {}:'.format(name))
    k2, p = normaltest(timeseries, axis=0, nan_policy='omit')
    print("p = {:g}".format(p))
    print("null hyp: series comes from a normal distribution")
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")


def lag_correlation_test(timeseries, name, lag=1):
    values = pd.DataFrame(timeseries.values)
    dataframe = pd.concat([values.shift(lag), values], axis=1)
    dataframe.columns = ['t-1', 't+1']
    result = dataframe.corr()
    print("Lag Correlation for {} = {}".format(name, result))


if __name__ == '__main__':
    path = os.path.join('.', 'data', 'raw', 'energy_dataset.csv')
    df = pd.read_csv(path)
    normal_test(df.loc[:, 'generation fossil oil'], 'generation biomass')
