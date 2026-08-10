from datetime import datetime,time,timedelta,date

now = datetime.now()
dateB = datetime.strptime('03-12-2003','%d-%m-%Y')
print(datetime.combine(now,time=time(8,59,50)))
print(now-dateB)
print(now + timedelta(60))