import numpy as np
import pandas as pd

################################################################################

# Read data 
trans = pd.read_excel('transactions.xlsx', sheet_name='Transactions', usecols=[0, 1, 2, 3, 4, 5])
# print trans.info()
# print trans.head(10)

################################################################################

# Sets the entries for each transaction
def set_entry(row):
    if row['Amount'] > 0:
        return 'Credit'
    else:
        return 'Debit'

# Calculates the balance
def calc_bal(amounts):
    data = []
    np.arange(amounts.size, dtype=np.float)
    for i in range(0, -amounts.size, -1):
        data.append(amounts.shift(i).sum())  
    return np.array(data)

# Finds the net for each transaction
def find_net(row):
    net = row['Sum_Credit'] + row['Sum_Debit']
    if net > 0:
        return 1
    elif net == 0:
        return 0
    else:
        return -1

# Creates a table on an index, columns, values, and function
def to_pivot_table(dataframe, index, columns, values, func):
    return pd.pivot_table(
        dataframe, index=index, 
        columns=columns, values=values, 
        aggfunc=func)

# Get subset of data by allocation number #
def write_data_by_alloc():
    by_alloc = trans.groupby('Allocation')
    writer = pd.ExcelWriter('allocations.xlsx', engine='xlsxwriter')
    for name, group in by_alloc:
        cols = ['Allocation','Date','Entry','Form','Category','Description','Amount']
        group.to_excel(writer, sheet_name=str(name), columns=cols)
    writer.save()
    
################################################################################

# Support data
dates = trans.loc[:,'Date']
trans.loc[:,'Balance'] = pd.Series(calc_bal(trans.loc[:,'Amount']), index=trans.index)
trans.loc[:,'Change_Balance'] = pd.Series(trans.loc[:,'Balance'].diff(), index=trans.index)
trans.loc[:,'Entry'] = pd.Series(trans.apply(set_entry, axis=1), index=trans.index)
trans.loc[:,'Time'] = pd.Series(dates.dt.time, index=trans.index)
trans.loc[:,'Day'] = pd.Series(dates.dt.dayofweek, index=trans.index)
trans.loc[:,'Month'] = pd.Series(dates.dt.month, index=trans.index)
trans.loc[:,'Year'] = pd.Series(dates.dt.year, index=trans.index)

################################################################################

# Transaction allocation
# write_data_by_alloc()
 
################################################################################

# Transactions by time
# Change in net per month
by_y_m = trans.groupby(['Year','Month'])
df_a = by_y_m['Amount'].agg([np.sum]).reset_index().rename(columns={'sum': 'Net'})
df_a.loc[:,'Change_Net'] = pd.Series(df_a['Net'].diff(), index=df_a.index)
# print df_a

# Change in net per year
by_m_y = trans.groupby(['Month','Year'])
df_b = by_m_y['Amount'].agg([np.sum]).reset_index().rename(columns={'sum': 'Net'})
df_b.loc[:,'Change_Net'] = pd.Series(df_b['Net'].diff(), index=df_b.index)
# print df_b

# Number of transactions per month in a given year
c = pd.DataFrame({'Count' : by_y_m.size()}).reset_index()
print c

################################################################################

# Transaction balance
bal = trans.loc[:,('Time', 'Balance')]
# print bal.head(1)
# print bal.min()
# print bal.max()

################################################################################

# Transaction amounts
# Keep only within (+n to -n) standard deviations from the mean    
n = [1, 2, 3]
col = trans.Amount
band = np.abs(col-col.mean())<=(n[0]*col.std())
amounts = trans.loc[:,'Amount'][band]

is_credit = (trans.Entry == 'Credit')
is_debit = (trans.Entry == 'Debit')

credits = amounts[is_credit]
# print credits.describe()
# print credits.sum()

debits = amounts[is_debit]
# print debits.describe()
# print debits.sum()

# Transaction credits/debits on the same date
t = trans
t.loc[:,'Date'] = pd.Series(dates.dt.date, index=trans.index)
by_date_entry = t.groupby(['Date', 'Entry'])
sum_a = by_date_entry['Amount'].agg([np.sum]).reset_index()

cred = (sum_a.Entry == 'Credit')
deb = (sum_a.Entry == 'Debit')
same_date = pd.merge(sum_a[cred], sum_a[deb], on='Date')
same_date = same_date.rename(columns={
    'Entry_x': 'Entry_Credit', 'Entry_y': 'Entry_Debit',
    'sum_x': 'Sum_Credit', 'sum_y': 'Sum_Debit'
})

same_date.loc[:,'Net'] = pd.Series(same_date.apply(find_net, axis=1))
# print same_date.head()

# Ratio of amount entries

################################################################################

# Transaction form
# Frequency 
form_freq = trans['Form'].value_counts(normalize=True)
# print (100*form_freq)

################################################################################

# Transaction category
# Frequency
cat_freq = trans['Category'].value_counts(normalize=True)
# print (100*cat_freq)

# Spendings & earnings of each category on frequency
by_cat = trans.groupby('Category')
sum_b = by_cat['Amount'].agg([np.sum])
# print sum_b.min()
# print sum_b.max()
# print sum_b

by_y_cat = trans.groupby(['Category', 'Year'])
sum_c = by_y_cat['Amount'].agg([np.sum])
# print sum_c.min()
# print sum_c.max()
# print sum_c

by_m_cat = trans.groupby(['Category', 'Month'])
sum_d = by_m_cat['Amount'].agg([np.sum])
# print sum_d.min()
# print sum_d.max()
# print sum_d

by_form_cat = trans.groupby(['Category', 'Form'])
# print by_form_cat.count()

################################################################################

