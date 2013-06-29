from django.template import Library

register = Library()

@register.filters
def row_grade(grade):
    a = int(grade)
    if grade < (a + 0.5):
        return  a
    if grade < a + 1:
        return a + 0,5
    return a + 1;

@register.filters
def remain_date(t):

    strDay = ' days'
    if t.days == 1:
        strDay = ' day'

    strHour = ' hours'
    hours = int(t.seconds/3600)
    if hours == 1:
        strHour = ' hour'
    if t.days:
        return t.days + strDay + ', ' + hours + strHour
    return hours + strHour