import pandas as pd

from transactions import calc_bal
################################################################################

# Read data 
cats = pd.read_excel('categories.xlsx', sheet_name=None)
# print cats.keys()
# for k, df in cats.items():
    # print df.info()
    # print df.head(3)

################################################################################

# Support data
for k, df in cats.items():
    dates = df.loc[:,'Date_Time']
    df.loc[:,'Balance'] = pd.Series(calc_bal(df.loc[:,'Amount']), index=df.index)
    df.loc[:,'Change_Balance'] = pd.Series(df.loc[:,'Balance'].diff(), index=df.index)
    df.loc[:,'Day'] = pd.Series(dates.dt.dayofweek, index=df.index)
    df.loc[:,'Month'] = pd.Series(dates.dt.month, index=df.index)
    df.loc[:,'Year'] = pd.Series(dates.dt.year, index=df.index)

################################################################################

# Allocation balance
for k, df in cats.items():
    cat_bal = df.loc[:,('Category','Date', 'Amount', 'Balance')]
    # print cat_bal.describe()
    # print cat_bal.head(1)
    # print cat_bal.min()
    # print cat_bal.max()
