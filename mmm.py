
from _datetime import datetime
from django.db.models.functions import (ExtractWeekDay)
from xdg.Exceptions import ValidationError

dt = datetime(2022, 3, 25, 10, 00, 00).date()

# print(dt.isoweekday())

# sch_from__lte=(a_from - datetime.timedelta(minutes=30)),

#
#
# dt= datetime.time(10, 00, 10)-datetime.timedelta(minutes=30)
#
print(dt)
