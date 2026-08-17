from datetime import datetime,time,timedelta,date
from zoneinfo import ZoneInfo

timeZone = ZoneInfo('Asia/Kolkata')
now = datetime.now(tz=timeZone)
dateB = datetime.strptime('03-08-2026','%d-%m-%Y')
dateB = dateB.replace(tzinfo=timeZone)
# print(datetime.combine(now,time=time(8,59,50)))
print(datetime.strftime(now,'%h:%m'))
print(now-dateB)
print(datetime.strftime(now + timedelta(days=1),'%d-%m-%Y'))


string = '03-12-2003'
print(datetime.strptime(string,'%Y-%'))