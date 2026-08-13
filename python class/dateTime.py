from datetime import datetime,time,timedelta,date
from zoneinfo import ZoneInfo

timeZone = ZoneInfo('Asia/Kolkata')
now = datetime.now(tz=timeZone)
dateB = datetime.strptime('03-12-2003','%d-%m-%Y')
dateB = dateB.replace(tzinfo=timeZone)
# print(datetime.combine(now,time=time(8,59,50)))
print(now-dateB)
print(now + timedelta(60))