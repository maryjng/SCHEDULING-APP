from datetime import datetime
from sqlalchemy import extract
import calendar

#database end
def get_month_appts():
    thismonth = datetime.today().month

    month_appts = Appointments.query.filter(extract('month', Appointments.date) == datetime.today().month).all
    return month_appts



#HTMLCalendar end
class monthcalendar(calendar.HTMLCalendar):
    year = datetime.today().year
    month = datetime.today().month

    def month_HTML(year=year, month=month):
        c = calendar.HTMLCalendar(calendar.Sunday)
        cal = c.formatmonth(year, month)
        return cal


calendar = monthcalendar()
c = calendar.month_HTML()
print(c)
