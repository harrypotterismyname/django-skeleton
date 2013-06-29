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
