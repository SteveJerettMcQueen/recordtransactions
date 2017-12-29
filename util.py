import datetime 
from random import randrange

# Generate random time from start date
def random_time(start):
    return start + datetime.timedelta(hours=randrange(24), minutes=randrange(60), seconds=randrange(60))

# Generate random time from a given date
def set_time(row):
    this_date = pd.to_datetime(row['Date'], format='%d-%m-%Y')
    return random_time(this_date)

# startDate = datetime.datetime(2013,9,15,13,00)
# print random_date(startDate).strftime("%m/%d/%y %H:%M")
