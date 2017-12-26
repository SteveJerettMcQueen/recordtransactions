import numpy as np
import pandas as pd
import pygal as pyg
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
# print plt.style.available
import seaborn as sns
import random as rnd

from util import random_time
################################################################################

# # # # Read data # # # # 
trans = pd.read_excel('transactions.xlsx', sheet_name='Transactions', usecols=[0, 1, 2, 3, 4, 5])
# print trans.info()
# print trans.head(10)

# # # # Functions on Dataframes # # # #
# Returns 1 if pos & 0 if neg
def find_sign(row):
    return 1 if row['Amount'] > 0 else 0

# Returns 1 if pos net & 0 if neg net
def find_pos_net(row):
    if((row['Credits'] + row['Debits']) > 0):
        return 1
    elif((row['Credits'] + row['Debits']) == 0):
        return 0
    else:
        return -1

def find_max(a, b):
    return a if (a > b) else b

# Generate random time for balance from a given date
# def set_time(row):
#     this_date = pd.to_datetime(row['Date'], format='%d-%m-%Y')
#     return random_time(this_date)

# Labels data for pygal tree map
# def to_labeled_pairs_tree_map(group_by_object):
    
#     labeled_pairs = []
#     for k, v in group_by_object.itertuples():
#         pair = {}
#         pair['value'] = v
#         pair['label'] = k
#         labeled_pairs.append(pair)
    
#     return labeled_pairs

# Labels data for pygal line chart
# def to_labeled_pairs_line_chart(balance):
    
#     labeled_pairs = []
#     for b in balance.values:
#         pair = {}
#         pair['value'] = b
#         pair['node'] = {'r': 0}
#         labeled_pairs.append(pair)
    
#     return labeled_pairs

# Calculate Data
def find_bal():
    data = []
    amounts = trans['Amount']
    np.arange(amounts.size, dtype=np.float)
    for i in range(0, -amounts.size, -1):
        data.append(amounts.shift(i).sum())  
    return np.array(data)
    
# # # # Extract Data from Dataframes # # # #
# trans['Date'] = pd.Series(trans.apply(set_time, axis=1), index=trans.index)# Temporary
trans.loc[:,'Balance'] = pd.Series(find_bal(), index=trans.index)
trans.loc[:,'Change_Balance'] = pd.Series(trans['Balance'].diff(), index=trans.index)
trans.loc[:,'Sign'] = pd.Series(trans.apply(find_sign, axis=1), index=trans.index)
trans.loc[:,'Time'] = pd.Series(trans['Date'].dt.time, index=trans.index)
trans.loc[:,'Day'] = pd.Series(trans['Date'].dt.dayofweek, index=trans.index)
trans.loc[:,'Month'] = pd.Series(trans['Date'].dt.month, index=trans.index)
trans.loc[:,'Year'] = pd.Series(trans['Date'].dt.year, index=trans.index)

###################################

col = 6
row = 10
# plt.figure(1)
# fig = plt.figure(figsize=(13,13))

# Transactions #
dy_table = pd.pivot_table(trans, index='Day', columns='Year', values='Amount', aggfunc='count')  
# print dy_table
# sns_heat_map = sns.heatmap(# Scale Data between 0 & 1
#     data=dy_table, vmin=1, vmax=129, annot=False, 
#     linewidths=.5, cbar_kws={"shrink": .75}, 
#     cmap='Blues')
# fig = sns_heat_map.get_figure()
# fig.savefig('display4.svg')

my_table = pd.pivot_table(trans, index='Month', columns='Year', values='Amount', aggfunc='count')  
# print my_table
# sns_heat_map = sns.heatmap(# Scale Data between 0 & 1
#     data=my_table, vmin=0, vmax=1, annot=False, 
#     linewidths=.5, cbar_kws={"shrink": .75}, 
#     cmap='Blues')
# fig = sns_heat_map.get_figure()
# fig.savefig('display4.svg')

dm_table = pd.pivot_table(trans, index='Day', columns='Month', values='Amount', aggfunc='count') 
# print dm_table
# sns_heat_map = sns.heatmap(# Scale Data between 0 & 1
#     data=dm_table, vmin=1, vmax=39, annot=False, 
#     linewidths=.5, cbar_kws={"shrink": .75}, 
#     cmap='Oranges')
# fig = sns_heat_map.get_figure()
# fig.savefig('display4.svg')

# Balance #
balance = trans[['Balance', 'Time']][::-1]
balance.set_index('Time')

change_bal = trans[['Change_Balance', 'Time']][::-1]
change_bal.set_index('Time')

# bpos = trans.Change_Balance > 0
# bneg = trans.Change_Balance < 0

# ax1 = plt.subplot2grid((row,col), (0,0), colspan=6, rowspan=3)
# ax1.set_xlabel('Time', fontsize=11)
# ax1.set_ylabel('Balance', fontsize=11)
# ax1.set_title('Balance over Time', fontsize=11)
# balance.plot(x='Time', y='Balance', ax=ax1)

# ax2 = plt.subplot2grid((row,col), (3,0), colspan=6, rowspan=3)
# ax2.set_xlabel('Time', fontsize=11)
# ax2.set_ylabel('Change in Balance', fontsize=11)
# ax2.set_title('Change in Balance over Time', fontsize=11)
# change_bal.plot(x='Time', y='Change_Balance', ax=ax2)

# chart = pyg.Line(fill=False)
# chart.title = 'Balance Over Time'
# chart.add('Balance', to_labeled_pairs_line_chart(balance['Balance'][::-1]))

# Amounts #
amounts = trans['Amount']
# amounts.describe()
# amounts.sum()

apos = trans.Amount > 0
aneg = trans.Amount < 0

credits = amounts[apos]
# credits.describe()
# credits.sum()

debits = amounts[aneg]
# debits.describe()
# debits.sum()

# # Keep only the ones that are within +n to -n standard deviations in the column    
n = [1, 2, 3]
band = np.abs(trans.Amount-trans.Amount.mean())<=(n[0]*trans.Amount.std())

# # Distribution on Amounts
# x    =  amounts[(band)]
# xmn  =  trans[['Month', 'Amount', 'Sign']][(band)]

# ax3 = plt.subplot2grid((row,col), (6,0), colspan=4, rowspan=4)
# ax3.set_xlabel('Amounts', fontsize=11)
# ax3.set_title('Distribution of Amounts', fontsize=11)
# sns_kde_plot = sns.kdeplot(x, shade=True, ax=ax3);
# # sns_dist_plot = sns.distplot(x, bins=750, kde=False, rug=False, ax=ax2);

# ax4 = plt.subplot2grid((row,col), (6,4), colspan=2, rowspan=2)
# ax4.set_xlabel('Credits', fontsize=11)
# ax4.set_title('Distribution of Credit Amounts', fontsize=11)
# sns_kde_plot = sns.kdeplot(x[apos], shade=True, ax=ax4);

# ax5 = plt.subplot2grid((row,col), (8,4), colspan=2, rowspan=2)
# ax5.set_xlabel('Debits', fontsize=11)
# ax5.set_title('Distribution of Debit Amounts', fontsize=11)
# sns_kde_plot = sns.kdeplot(x[aneg], shade=True, ax=ax5);

# Save Plot Data #
# plt.tight_layout()
# fig.savefig("display.svg")

###################################

# row = 14
# plt.figure(2)
# fig2 = plt.figure(figsize=(13,13))

xdtp =  trans[['Date', 'Amount', 'Category']][(band) & (apos)]
xdtp['Date'] = pd.Series(trans['Date'].dt.date, index=trans.index)
xdtn =  trans[['Date', 'Amount', 'Category']][(band) & (aneg)]
xdtn['Date'] = pd.Series(trans['Date'].dt.date, index=trans.index)
xdtp =  xdtp.rename(columns={'Amount': 'Credits'})
xdtn =  xdtn.rename(columns={'Amount': 'Debits'})

g = xdtp.groupby('Date')
df_c = g['Credits'].agg(np.sum).reset_index()

g2 = xdtn.groupby('Date')
df_d = g2['Debits'].agg(np.sum).reset_index()
xdtsp_n = pd.merge(df_c, df_d, on='Date')

xdtsp_n.loc[:,'Pos_Net'] = pd.Series(xdtsp_n.apply(find_pos_net, axis=1))
xdtsp_n['Debits'] = xdtsp_n.Debits.abs()
# print xdtsp_n

# ax6 = plt.subplot2grid((row,col), (0,0), colspan=6, rowspan=4)
# ax6.set_title("Amount Values Scattered Per Month")
# sns_swarm_plot = sns.swarmplot(x='Month', y='Amount', hue='Sign', data=xmn.abs(), ax=ax6);

# ax7 = plt.subplot2grid((row,col), (4,1), colspan=2, rowspan=5)
# ax7.set_xlabel('Year', fontsize=11)
# ax7.set_ylabel('Month', fontsize=11)
# ax7.set_title("Percentage of Credits")
# sns_heat_map = sns.heatmap(
#     credits_matrix.T, vmin=0, vmax=1, annot=False, 
#     linewidths=.5, square=False, cbar_kws={"shrink": .75}, 
#     cmap='Oranges', ax=ax7)

# ax8 = plt.subplot2grid((row,col), (4,3), colspan=2, rowspan=5)
# ax8.set_title("Percentage of Debits")
# ax8.set_xlabel('Year', fontsize=11)
# ax8.set_ylabel('Month', fontsize=11)
# sns_heat_map = sns.heatmap(
#     debits_matrix.T, vmin=0, vmax=1, annot=False, 
#     linewidths=.5, square=False, cbar_kws={"shrink": .75}, 
#     cmap='Blues', ax=ax8)

# ax9 = plt.subplot2grid((row,col), (9,1), colspan=4, rowspan=5)
# ax9.set_xlabel('Credits', fontsize=11)
# ax9.set_ylabel('Debits', fontsize=11)
# ax9.set_title('Relationship Between Credits and Debits')
# g = sns.jointplot(data=xdtsp_n, x='Credits', y='Debits', kind="kde", cmap='Purples');
# g = sns.jointplot(data=xdtsp_n, x='Credits', y='Debits', kind='reg');
# g = sns.lmplot(data=xdtsp_n, x='Credits', y='Debits', hue='Pos_Net',
#     x_jitter=50,  y_jitter=50, aspect=1.25)

# g.savefig("display5.svg")

# Save Plot Data #
# fig2.savefig("display2.svg")

###################################

# row = 10
# plt.figure(3)
# fig3 = plt.figure(figsize=(20,30))

# Frequency on Form #
fvc = trans['Form'].value_counts(normalize=True)
# print (100*fvc)

group_b = trans.groupby(['Form', 'Category'])
# print group_b['Allocation'].count()

# x = trans.sort_values(by=['Category'])
# ax10 = plt.subplot2grid((row,col), (0,0), colspan=6, rowspan=4)
# ax10.set_ylabel('Category', fontsize=11)
# ax10.set_title("Forms for each Category")
# sns_plot = sns.countplot(y="Category", hue="Form", data=x, palette="Greens_d", ax=ax10);

# ax11 = plt.subplot2grid((row,col), (5,0), colspan=6, rowspan=4)
# ax11.set_ylabel('Form', fontsize=11)
# ax11.set_title("Categories for each Form")
# sns_plot = sns.countplot(x="Form", hue="Category", data=x, palette="Blues_d", ax=ax11);

# Save Plot Data #
# fig3.savefig("display3.svg")

# Frequency on Categories #
cvc = trans['Category'].value_counts(normalize=True)
# print (100*cvc)

# Spending & Earnings of Each Category #
# df_filt = trans.groupby("Category").filter(lambda x: len(x) > 1)
# group_filt = df_filt.groupby('Category')
# by_amount = group_filt['Amount']

group_cat = trans.groupby('Category')
by_amount = group_cat['Amount']
sum_amt = by_amount.agg([np.sum])
# print by_amount.count()
# print sum_amt

group_cat_y = trans.groupby(['Year', 'Category'])
by_amount_y = group_cat_y['Amount']
sum_amt_y = by_amount_y.agg([np.sum])
# print by_amount_y.count()
# print sum_amt_y

# fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(12,10))
# cat_table = pd.pivot_table(trans, index='Category', columns='Year', values='Amount', aggfunc=np.sum)    
# print cat_table
# sns_heat_map = sns.heatmap(
#     cat_table, vmin=0, vmax=15000, annot=False, 
#     linewidths=.5, square=False, cbar_kws={"shrink": .75}, 
#     cmap='Blues', ax=ax)
# fig.savefig('display7.svg')

group_b = trans.groupby(['Category', 'Form'])
# print group_b['Allocation'].count()

# cash = trans.Form == 'Cash'
# electronic = trans.Form == 'Electronic'
# tfc = trans[['Form', 'Category']]
# fcc = tfc[cash].groupby('Category').count()
# fce = tfc[electronic].groupby('Category').count()

# chart = pyg.Treemap()
# chart.title = 'Form & Category TreeMap'
# chart.add('Electorinic', to_labeled_pairs_tree_map(fce))
# chart.add('Cash', to_labeled_pairs_tree_map(fcc))
# chart.render_to_file('treemap.svg')

# Net Change Per Month #
grouped = trans.groupby(['Year','Month'])
df = grouped['Amount'].agg([np.sum]).reset_index().rename(columns={'sum': 'Net'})
df.loc[:,'Change_Net'] = pd.Series(df['Net'].diff(), index=df.index)
# print df
    
sum_table = pd.pivot_table(trans, index='Month', columns='Year', values='Amount', aggfunc=np.sum)    
# print sum_table
# sns_heat_map = sns.heatmap(
#     sum_table, vmin=0, vmax=1, annot=False, 
#     linewidths=.5, square=False, cbar_kws={"shrink": .75}, 
#     cmap='Blues')
# fig = sns_heat_map.get_figure()
# fig.savefig('display4.svg')

# NUmber of Transactions Per Month in A Given Year #
# c = pd.DataFrame({'Count' : grouped.size()}).reset_index()
# print c
    
# Get subset of data on Allocation Number #
# grouped_alloc = trans.groupby('Allocation')
# writer = pd.ExcelWriter('allocations.xlsx', engine='xlsxwriter')
# for name, group in grouped_alloc:
#     cols = ['Allocation','Date','Form','Category','Description','Amount']
#     group.to_excel(writer, sheet_name=str(name), columns=cols)
# writer.save()
