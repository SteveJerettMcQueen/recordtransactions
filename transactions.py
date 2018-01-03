import numpy as np
import pandas as pd

from scipy.stats import chi2_contingency
################################################################################

# Read data 
trans = pd.read_excel('transactions.xlsx', sheet_name='Transaction', usecols=[0, 1, 2, 3, 4])
# print trans.info()
# print trans.head()

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

# Get subset of data by category #
def write_data_by_category():
    by_cat = trans.groupby('Category')
    writer = pd.ExcelWriter('categories.xlsx', engine='xlsxwriter')
    for name, group in by_cat:
        cols = ['Date_Time','Entry','Form','Category','Description','Amount']
        group.to_excel(writer, sheet_name=str(name), columns=cols)
    writer.save()
    
################################################################################

# Support data
dates = trans.loc[:,'Date_Time']
# trans.loc[:,'Date_Time'] = pd.Series(trans.apply(ut.set_time, axis=1), index=trans.index)
trans.loc[:,'Balance'] = pd.Series(calc_bal(trans.loc[:,'Amount']), index=trans.index)
trans.loc[:,'Change_Balance'] = pd.Series(trans.loc[:,'Balance'].diff(), index=trans.index)
trans.loc[:,'Entry'] = pd.Series(trans.apply(set_entry, axis=1), index=trans.index)
trans.loc[:,'Day'] = pd.Series(dates.dt.dayofweek, index=trans.index)
trans.loc[:,'Month'] = pd.Series(dates.dt.month, index=trans.index)
trans.loc[:,'Year'] = pd.Series(dates.dt.year, index=trans.index)

################################################################################

# Transaction category
# write_data_by_category()
 
################################################################################

# Transactions by time
# Change in net per month
by_y_m = trans.groupby(['Year','Month'])
by_year_month = by_y_m['Amount'].agg([np.sum]).reset_index().rename(columns={'sum':'Net'})
by_year_month.loc[:,'Change_Net'] = pd.Series(by_year_month['Net'].diff(), index=by_year_month.index)
# print by_year_month

# Change in net per year
by_m_y = trans.groupby(['Month','Year'])
by_month_year = by_m_y['Amount'].agg([np.sum]).reset_index().rename(columns={'sum':'Net'})
by_month_year.loc[:,'Change_Net'] = pd.Series(by_month_year['Net'].diff(), index=by_month_year.index)
# print by_month_year

# Number of transactions per month in a given year
per_month_year = pd.DataFrame({'Count' : by_y_m.size()}).reset_index()
# print per_month_year

################################################################################

# Transaction balance
curr_bal = trans['Balance'].iloc[0]
min_bal = trans['Balance'].min()
max_bal = trans['Balance'].max()

# print curr_bal

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
t = trans[band]
u = t.assign(Date = lambda x: x.loc[:,'Date_Time'].dt.date)
by_date_entry = u.groupby(['Date', 'Entry'])

sum_a = by_date_entry['Amount'].agg([np.sum]).reset_index()
cred = (sum_a.Entry == 'Credit')
deb = (sum_a.Entry == 'Debit')

on_same_date = pd.merge(sum_a[cred], sum_a[deb], on='Date')
on_same_date = on_same_date.rename(columns={
    'Entry_x': 'Entry_Credit', 'Entry_y': 'Entry_Debit',
    'sum_x': 'Sum_Credit', 'sum_y': 'Sum_Debit'
})

on_same_date.loc[:,'Net'] = pd.Series(on_same_date.apply(find_net, axis=1))
# print on_same_date.head()

# Transaction entry
# Fequency of amount entries
ent_freq = trans.loc[:,'Entry'].value_counts(normalize=True)
# print (100*ent_freq)

# ################################################################################

# Transaction form
# Frequency 
form_freq = trans.loc[:,'Form'].value_counts(normalize=True)
# print (100*form_freq)

# ################################################################################

# Transaction category
# Frequency
cat_freq = trans.loc[:,'Category'].value_counts(normalize=True)
# print (100*cat_freq)

# Spendings & earnings of each category on frequency
by_cat = trans.groupby('Category')
by_category = by_cat['Amount'].agg([np.sum])
# print by_category.min()
# print by_category.max()
# print by_category

by_y_cat = trans.groupby(['Category', 'Year'])
by_year_category = by_y_cat['Amount'].agg([np.sum])
# print by_year_category.min()
# print by_year_category.max()
# print by_year_category

by_m_cat = trans.groupby(['Category', 'Month'])
by_month_category = by_m_cat['Amount'].agg([np.sum])
# print by_month_category.min()
# print by_month_category.max()
# print by_month_category

by_form_cat = trans.groupby(['Category', 'Form'])
# print by_form_cat.count()

# Credit categories
cc = trans.loc[:,('Category', 'Amount')][is_credit]
by_c_c = cc.groupby('Category')
by_credit_cats = by_c_c['Amount'].agg([np.sum])
# print by_credit_cats.min()
# print by_credit_cats.max()
# print by_credit_cats

# Debit categories
dc = trans.loc[:,('Category', 'Amount')][is_debit]
by_d_c = dc.groupby('Category')
by_debit_cats = by_d_c['Amount'].agg([np.sum])
# print by_debit_cats.min()
# print by_debit_cats.max()
# print by_debit_cats

# ################################################################################

# Test for categorical independency of transactions
contingency = pd.crosstab(trans.Category, trans.Entry)
# print contingency
chi2, p, dof, exp = chi2_contingency(contingency)
# print p
