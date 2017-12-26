from random import randrange
import datetime 

value = 1

# Generate random time from start date
def random_time(start):
    return start + datetime.timedelta(hours=randrange(24), minutes=randrange(60), seconds=randrange(60))

# startDate = datetime.datetime(2013,9,15,13,00)
# print random_date(startDate).strftime("%m/%d/%y %H:%M")
