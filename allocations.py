import pandas as pd

from transactions import calc_bal
################################################################################

# Read data 
allocs = pd.read_excel('allocations.xlsx', sheet_name=None)
# print allocs.keys()
# for k, df in allocs.items():
    # print df.info()
    # print df.head(3)

################################################################################

# Note allocations as of 12/28/17
# 1000 Transportation       52          6/2/15
# 2000 Gifts & Donations    248.79      1/29/15
# 3000 Food & Dining        100         2/16/15
# 4000 Personal Care        55          1/4/15
# 5000 Bills & Utilities    0           12/9/14
# 6000 Savings              4478.93     10/1/14 | 4478.93
# 8000 Sinking Fund         4138.87     10/1/14 | 4487.66
# 9000 Education Fund       0           8/13/12

# Support data
for k, df in allocs.items():
    dates = df.loc[:,'Date']
    df.loc[:,'Balance'] = pd.Series(calc_bal(df.loc[:,'Amount']), index=df.index)
    df.loc[:,'Change_Balance'] = pd.Series(df.loc[:,'Balance'].diff(), index=df.index)
    df.loc[:,'Day'] = pd.Series(dates.dt.dayofweek, index=df.index)
    df.loc[:,'Month'] = pd.Series(dates.dt.month, index=df.index)
    df.loc[:,'Year'] = pd.Series(dates.dt.year, index=df.index)

################################################################################

# Allocation balance
for k, df in allocs.items():
    alloc_bal = df.loc[:,('Allocation','Date', 'Amount', 'Balance')]
    # print alloc_bal.describe()
    print alloc_bal.head(1)
    # print alloc_bal.min()
    # print alloc_bal.max()
