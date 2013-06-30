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
def remain_date(value):
    if value:
        strDay = ' days'
        if value.days == 1:
            strDay = ' day'

        strHour = ' hours'
        hours = int(value.seconds / 3600)
        if hours == 1:
            strHour = ' hour'

        if value.days > 0 or hours > 0:
            return str(value.days) + strDay + ', ' + str(hours) + strHour

        return ''
    else:
        return ''