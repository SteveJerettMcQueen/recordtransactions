import numpy as np
import pandas as pd
import matplotlib as mpl
mpl.use('agg')
import matplotlib.pyplot as plt
plt.style.use('seaborn-darkgrid')
import matplotlib.dates as mdates

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import seaborn as sns

import earnings as ear

from util import to_pivot_table

################################################################################

# Heatmaps

# Map month and year on sum
def save_heat_map_f():
    fig = plt.figure(figsize=(7, 7))
    d = to_pivot_table(ear.earns,'Month','Year','Net_Pay', np.sum)   
    ax = sns.heatmap(data=d, vmin=d.min().min(), vmax=d.max().max(), 
        annot=True, fmt='.2f', linewidths=.5, cbar=True,
        cbar_kws={"shrink": 1}, cmap='BuPu')
    ax.set_title('Sum Of Net Pay Per Month', fontsize=11)
    ax.set_xlabel('Year', fontsize=11)
    ax.set_ylabel('Month', fontsize=11)
    fig = ax.get_figure()
    fig.savefig('graphs/heatmap_f.svg')

# Line charts

# Chart on net pay
def save_line_chart_c():
    fig, axes = plt.subplots(figsize=(10, 4))
    for k, df in ear.by_workplace:
        ax = df.plot(x='Check_Date', y='Net_Pay', kind='line', ax=axes, label=k)
        ax.set_title('Net Pay over Time', fontsize=11)
        ax.set_xlabel('Date', fontsize=11)
        ax.set_ylabel('Net Pay', fontsize=11)

    fig = ax.get_figure()
    fig.savefig('graphs/line_chart_c.svg')

def save_line_chart_c_plotly():
    data = []
    for k, df in ear.by_workplace:
        data.append(
            go.Scatter(
                name=k,
                x=df['Check_Date'], 
                y=df['Net_Pay'],
                fill='tozeroy'
            )
        )
        
    layout = go.Layout(
        title='Net Pay over Time',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Net Pay'),
        autosize=False,
        width=1000,
        height=500
    )
    
    py.image.save_as({'data': data, 'layout': layout}, 'graphs/line_chart_c_plotly.jpeg')

################################################################################

# Univariate histograms

x = ear.earns['Net_Pay']

# Histogram of net pay
def save_hist_e():
    fig = plt.figure(figsize=(10, 7))
    ax = sns.kdeplot(x, shade=True)
    ax.set_xlabel('Net Pay', fontsize=11)
    ax.set_title('Distribution of Net Pay', fontsize=11)
    
    fig = ax.get_figure()
    fig.savefig('graphs/histogram_e.svg')

################################################################################

def save_figs():
    save_heat_map_f()
    save_line_chart_c()
    save_line_chart_c_plotly()
    save_hist_e()
    