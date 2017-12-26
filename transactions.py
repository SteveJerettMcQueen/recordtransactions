import random as rand
import numpy as np
import pandas as pd
import pygal
import matplotlib as mpl
mpl.use('template')
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import chi2_contingency

################################################################################
'''''
get chi-test on categories & amount(binary)
piechart on debit/consumption
piechart on credit/income
ratio of credits to debits

'''''
def is_pos(row):
    return 1 if row['Amount'] > 0 else 0

trans = pd.read_excel('transactions.xlsx', sheet_name='Sheet1', usecols=[0, 1, 2, 3, 4, 5])
# print trans.describe()
# print trans.dtypes
# print trans.info()
# print trans

# Total Amounts
amounts = trans['Amount'];
# print amounts.diff()
# print amounts.sum()

# sns_plot = sns.kdeplot(amounts, shade=True);
sns_plot = sns.distplot(amounts);
fig = sns_plot.get_figure()
fig.savefig("display.svg")

# Total Credits
is_credit = (trans.Amount > 0)
credits = amounts[is_credit]
# print credits.diff()
# print credits.sum()

# Total Debits
is_debit = (trans.Amount < 0)
debits = amounts[is_debit]
# print debits.diff()
# print debits.sum()

# Get on Allocation
# alloc = trans['Allocation'][(trans.Allocation == 10000)]
# print alloc

# Get Corresponding Day of Week
# trans['Weekday'] = trans['Date'].dt.dayofweek
# trans['Pos'] = trans.apply(is_pos, axis=1)
# t = trans[['Weekday','Amount', 'Pos']].abs()

# wt = trans[['Weekday', 'Amount']][is_debit].groupby('Weekday')
# wtc = wt.count()
# print wtc
# sns_plot = sns.swarmplot(x="Weekday", y="Amount", hue='Pos', data=t);
# fig = sns_plot.get_figure()
# fig.savefig("display.svg")

# Frequency on Amounts
# a = trans[['Category', 'Amount']]
# a2 = a[is_debit].groupby('Amount')
# a2c = a2.count()
# print a2c

# Percentage of Categories of Transactions
# pc = trans['Category'].value_counts(normalize=True)
# print (100*pc)

# Frequency on Categories
# s = trans[['Category', 'Amount']]
# s2 = s[is_credit].groupby('Category')
# s2c = s2.count()
# print s2c

# s3 = s[is_debit].groupby('Category')
# s3c = s3.count()
# print s3c

# sns_plot = sns.countplot(x="Category", hue="Form", data=trans, palette="Greens_d");
# fig = sns_plot.get_figure()
# fig.savefig("display.svg")

# # Contigency table
# # Categorize the amount to either 1 or 0
# trans['Pos'] = trans.apply(is_pos, axis=1)

# # Chi-square test of independence
# contigency = pd.crosstab(trans['Category'], trans['Pos'])
# print contigency

# c, p, dof, exp = chi2_contingency(contigency)
# print (c, p, dof)
# print exp

# Frequencies on Form
s4 = trans[['Form', 'Category', 'Amount']]
s5 = s4[is_credit].groupby('Category')
# s5c = s5.count()
# print s5c
# print s5c.loc['Cash','Category']
# print s5c.loc['Electronic','Category']

# s6 = s4[is_debit].groupby('Form')
# s6c = s6.count()
# print s6c
# print s6c.loc['Cash','Category']
# print s6c.loc['Electronic','Category']

# Get transactions by Date 
# s7c = trans['Amount'][is_credit & (trans.Date >= '1/1/2012') & (trans.Date <= '12/31/2012')]
# s7d = trans['Amount'][is_debit & (trans.Date >= '1/1/2012') & (trans.Date <= '12/31/2012')]
# s8c = trans['Amount'][is_credit & (trans.Date >= '1/1/2013') & (trans.Date <= '12/31/2013')]
# s8d = trans['Amount'][is_debit & (trans.Date >= '1/1/2013') & (trans.Date <= '12/31/2013')]
# s9c = trans['Amount'][is_credit & (trans.Date >= '1/1/2014') & (trans.Date <= '12/31/2014')]
# s9d = trans['Amount'][is_debit & (trans.Date >= '1/1/2014') & (trans.Date <= '12/31/2014')]
# s10c = trans['Amount'][is_credit & (trans.Date >= '1/1/2015') & (trans.Date <= '12/31/2015')]
# s10d = trans['Amount'][is_debit & (trans.Date >= '1/1/2015') & (trans.Date <= '12/31/2015')]
# s11c = trans['Amount'][is_credit & (trans.Date >= '1/1/2016') & (trans.Date <= '12/31/2016')]
# s11d = trans['Amount'][is_debit & (trans.Date >= '1/1/2016') & (trans.Date <= '12/31/2016')]
# s12c = trans['Amount'][is_credit & (trans.Date >= '1/1/2017') & (trans.Date <= '12/31/2017')]
# s12d = trans['Amount'][is_debit & (trans.Date >= '1/1/2017') & (trans.Date <= '12/31/2017')]
# print(s7c.sum(), s7d.sum())
# print(s8c.sum(), s8d.sum())
# print(s9c.sum(), s9d.sum())
# print(s10c.sum(), s10d.sum())
# print(s11c.sum(), s11d.sum())
# print(s12c.sum(), s12d.sum())

# chart = pygal.HorizontalBar()
# chart.title = 'Category Data'
# for k, v in s.groupby('Category').count().itertuples():
#     chart.add(k, v)
# chart.render_to_file('routes.svg')
