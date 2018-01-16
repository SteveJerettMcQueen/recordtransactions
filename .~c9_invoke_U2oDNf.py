import numpy as np
import pandas as pd
import finances as fin

################################################################################

# Read data 
earns = fin.earnings
# print earns.info()
# print earns.head()

################################################################################

# Calculates the taxes from the gross and net pay
def calc_tax(row):
    return row['Gross_Pay'] - row['Net_Pay']

################################################################################

# Support data
dates = earns.loc[:,'Check_Date']
earns.loc[:,'Tax'] = pd.Series(earns.apply(calc_tax, axis=1), index=earns.index)
earns.loc[:,'Day'] = pd.Series(dates.dt.dayofweek, index=earns.index)
earns.loc[:,'Month'] = pd.Series(dates.dt.month, index=earns.index)
earns.loc[:,'Year'] = pd.Series(dates.dt.year, index=earns.index)

################################################################################

# Taxes
# print earns.loc[:,'Tax']

# Earnings by place of work
by_workplace = earns.groupby('Workplace')
# print by_workplace.count()

by_workplace_stats = by_workplace[['Gross_Pay','Net_Pay','Tax']].agg([np.sum, np.mean, np.std])
# print by_workplace_stats

# Earnings description
# for k, df in by_workplace:
#     print df.describe()
