import numpy as np
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
import seaborn as sns
import matplotlib.dates as mdates
import transactions as tr

################################################################################

# Heatmaps

# Map day and year on count
def save_heat_map_a():
    fig = plt.figure(figsize=(7, 7))
    a = tr.to_pivot_table(tr.trans,'Day','Year','Amount','count')
    ax = sns.heatmap(data=a, 
        vmin=a.min().min(), vmax=a.max().max(), annot=True, fmt='.2f',
        linewidths=.5, cbar_kws={"shrink": .80}, cmap='Blues')
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_a.svg')

# Map month and year on count
def save_heat_map_b():
    fig = plt.figure(figsize=(7, 7))
    b = tr.to_pivot_table(tr.trans,'Month','Year','Amount','count')
    ax = sns.heatmap(data=b, 
        vmin=b.min().min(), vmax=b.max().max(), annot=True, fmt='.2f',
        linewidths=.5, cbar_kws={"shrink": .80}, cmap='Blues')
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_b.svg')

# Map day and month on count
def save_heat_map_c():
    fig = plt.figure(figsize=(7, 7))
    c = tr.to_pivot_table(tr.trans,'Day','Month','Amount','count')
    ax = sns.heatmap(data=c, 
        vmin=c.min().min(), vmax=c.max().max(), annot=True, 
        linewidths=.5, cbar_kws={"shrink": .80}, cmap='Blues')
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_c.svg')

# Map month and year on sum
def save_heat_map_d():
    fig = plt.figure(figsize=(7, 7))
    d = tr.to_pivot_table(tr.trans,'Month','Year','Amount', np.sum)   
    ax = sns.heatmap(data=d, 
        vmin=d.min().min(), vmax=d.max().max(), annot=True, fmt='.2f',
        linewidths=.5, cbar_kws={"shrink": .80}, cmap='Blues')
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_d.svg')

# Map category and year on sum
def save_heat_map_e():
    fig = plt.figure(figsize=(9,12))
    e = tr.to_pivot_table(tr.trans,'Category','Year','Amount', np.sum)    
    ax = sns.heatmap(data=e, 
        vmin=e.min().min(), vmax=e.max().max(), annot=True, fmt='.2f',
        linewidths=.5, cbar_kws={"shrink": .80}, cmap='Blues')
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_e.svg')

################################################################################

# Line charts
years = mdates.YearLocator()  
months = mdates.MonthLocator()  
yearsFmt = mdates.DateFormatter('%Y')
start_date = tr.trans.Date >= '1/1/2015'

# Chart on balance
def save_line_chart_a():
    bal = tr.trans[['Balance','Date']][start_date][::-1]
    bal.set_index('Date')
    
    ax = bal.plot(x='Date', y='Balance', figsize=(16, 6))
    ax.set_title('Balance over Time', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Balance', fontsize=11)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    fig = ax.get_figure()
    fig.savefig('graphs/line_chart_a.svg')

# Chart on change in balance
def save_line_chart_b():
    change_bal = tr.trans[['Change_Balance','Date']][start_date][::-1]
    change_bal.set_index('Date')
    
    ax = change_bal.plot(x='Date', y='Change_Balance', figsize=(16, 6))
    ax.set_title('Change in Balance over Time', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Change in Balance', fontsize=11)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(yearsFmt)
    ax.xaxis.set_minor_locator(months)

    fig = ax.get_figure()
    fig.savefig('graphs/line_chart_b.svg')

################################################################################

# Univariate histograms

x = tr.trans['Amount'][tr.band]

# Histogram of amounts
def save_hist_a():
    fig = plt.figure(figsize=(10, 7))
    ax3 = sns.kdeplot(x, shade=True)
    # ax3 = sns.distplot(x, bins=20, kde=False, vertical=True)
    ax3.set_xlabel('Amounts', fontsize=11)
    ax3.set_title('Distribution of Amounts', fontsize=11)
    
    fig = ax3.get_figure()
    fig.savefig('graphs/histogram_a.svg')

# Histogram of credits
def save_hist_b():
    fig = plt.figure(figsize=(8, 4))
    y = x[tr.trans.Entry == 'Credit']
    y.rename(columns={'Amount':'Credits'})
    ax4 = sns.kdeplot(y, shade=True)
    # ax4 = sns.distplot(y, bins=20, kde=False, vertical=True)
    ax4.set_xlabel('Credit', fontsize=11)
    ax4.set_title('Distribution of Credits', fontsize=11)
    
    fig = ax4.get_figure()
    fig.savefig('graphs/histogram_b.svg')

# Histogram of debits
def save_hist_c():
    fig = plt.figure(figsize=(8, 4))
    z = x[tr.trans.Entry == 'Debit'].abs()
    z.rename(columns={'Amount':'Debit'})
    ax5 = sns.kdeplot(z, shade=True)
    # ax5 = sns.distplot(z, bins=20, kde=False, vertical=True)
    ax5.set_xlabel('Debits', fontsize=11)
    ax5.set_title('Distribution of Debits', fontsize=11)
    
    fig = ax5.get_figure()
    fig.savefig('graphs/histogram_c.svg')

# Bivariate histogram

y = tr.on_same_date

# Histogram of credits and debits
def save_hist_d():
    y.loc[:,'Sum_Debit'] = y.Sum_Debit.abs()
    ax = sns.jointplot(data=tr.on_same_date, x='Sum_Credit', y='Sum_Debit',
        kind="kde", size=6, ratio=4, cmap='Blues');
    ax.savefig('graphs/histogram_d.svg')
    
# Regression plot of credits and debits
def save_reg_a():
    y.loc[:,'Sum_Debit'] = y.Sum_Debit.abs()
    ax = sns.lmplot(data=tr.on_same_date, x='Sum_Credit', y='Sum_Debit', hue='Net', 
        x_jitter=40,  y_jitter=40, size=6, aspect=1.75)
    ax.savefig('graphs/regression_a.svg')
    
################################################################################

# Categorical charts
# Scatter of transactions for each month on entry
def save_scat_a():
    fig = plt.figure(figsize=(15, 6))
    data = tr.trans[['Month', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.swarmplot(data=data, x='Month', y='Amount', hue='Entry', dodge=True, size=3.5);
    
    fig = ax.get_figure()
    fig.savefig('graphs/scatter_a.svg')

# Scatter of transactions for each month of a given year on entry
def save_fact_a():
    data = tr.trans[['Month', 'Year', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.factorplot(data=data, x="Month", y="Amount", hue="Entry", 
        col="Year", kind="swarm", size=6, aspect=.7, col_wrap=2);
    ax.savefig('graphs/factor_a.svg')

# Scatter of transactions for each month of a given year on category
def save_fact_b():
    data = tr.trans[['Month', 'Category', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.factorplot(data=data, x="Month", y="Amount", hue="Entry", 
        col="Category", kind="swarm", size=3, aspect=1, col_wrap=4);
    ax.savefig('graphs/factor_b.svg')

# Box of transactions for each day 
def save_box_a():
    fig = plt.figure(figsize=(12, 6))
    data = tr.trans[['Day', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.boxplot(data=data, x='Day', y='Amount', hue='Entry');
    
    fig = ax.get_figure()
    fig.savefig('graphs/box_a.svg')

# Box of transactions for each month 
def save_box_b():
    fig = plt.figure(figsize=(15, 6))
    data = tr.trans[['Month', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.boxplot(data=data, x='Month', y='Amount', hue='Entry');
    
    fig = ax.get_figure()
    fig.savefig('graphs/box_b.svg')
    
# Box of transactions for each year 
def save_box_c():
    fig = plt.figure(figsize=(9, 8))
    data = tr.trans[['Year', 'Amount', 'Entry']][tr.band]
    data['Amount'] = data['Amount'].abs()
    ax = sns.boxplot(data=data, x='Year', y='Amount', hue='Entry');
    
    fig = ax.get_figure()
    fig.savefig('graphs/box_c.svg')

# Count of transactions of each form and category
def save_count_a():
    fig = plt.figure(figsize=(12, 12))
    ax = sns.countplot(data=tr.trans, x="Form", hue="Category", palette="Blues_d");
    
    fig = ax.get_figure()
    fig.savefig('graphs/count_a.svg')

# Count of transactions of each form and entry
def save_count_b():
    fig = plt.figure(figsize=(12, 4))
    ax = sns.countplot(data=tr.trans, y="Form", hue="Entry", palette="Blues_d");
    
    fig = ax.get_figure()
    fig.savefig('graphs/count_b.svg')
    
################################################################################

def save_figs():
    save_heat_map_a()
    save_heat_map_b()
    save_heat_map_c()
    save_heat_map_d()
    save_heat_map_e()
    # save_line_chart_a()
    # save_line_chart_b()
    # save_hist_a()
    # save_hist_b()
    # save_hist_c()
    # save_hist_d()
    # save_reg_a()
    # save_scat_a()
    # save_fact_a()
    # save_fact_b()
    # save_box_a()
    # save_box_b()
    # save_box_c()
    # save_count_a()
    # save_count_b()

save_figs()