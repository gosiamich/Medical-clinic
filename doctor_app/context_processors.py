from datetime import datetime
import time

def get_date(request):
    return {'date':datetime.now().date()}