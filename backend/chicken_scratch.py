import datetime
current_time_minus_X = datetime.timedelta(minutes=4)
current_time_minus_X = (datetime.datetime.now() - current_time_minus_X)
print current_time_minus_X.now()
print datetime.datetime.now()