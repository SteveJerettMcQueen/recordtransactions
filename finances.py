import pandas as pd

################################################################################

# Data file
xlsx = pd.ExcelFile('finances.xlsx')

# Read data 
trans = pd.read_excel(xlsx, 'Transactions', usecols=[0, 1, 2, 3, 4])
earnings = pd.read_excel(xlsx, 'Earnings', usecols=[0, 1, 2, 3])

################################################################################

