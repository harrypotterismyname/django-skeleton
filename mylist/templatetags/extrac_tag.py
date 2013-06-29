from django.template import Library

register = Library()

@register.filter
def row_grade(grade):
    a = int(grade)
    if grade < (a + 0.5):
        return  a
    if grade < a + 1:
        return a + 0,5
    return a + 1

import  datetime
@register.filter
def remain_date(t):
    if t:
        strDay = ' days'
        if datetime.timedelta(t).days == 1:
            strDay = ' day'

        strHour = ' hours'
        hours = int(t.seconds / 3600)
        if hours == 1:
            strHour = ' hour'

        if t.days:
            return str(t.days) + strDay + ', ' + str(hours) + strHour

        return str(hours) + strHour
    else:
        return '0 days'