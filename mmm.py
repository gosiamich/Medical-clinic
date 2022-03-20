# The week_day lookup_type is calculated differently from most databases and from Python’s standard functions.
# This function will return 1 for Sunday, 2 for Monday, through 7 for Satur
#
from _datetimeimport datetime
from django.db.models.functions import (ExtractWeekDay)
from xdg.Exceptions import ValidationError

# dt = datetime(2022, 3, 25)
# time2 = datetime.time(10)
# print(dt.isoweekday())
print(time2)
# sch_from__lte=(a_from - datetime.timedelta(minutes=30)),



dt= datetime.time(10, 00, 10)-datetime.timedelta(minutes=30)

print(dt)
