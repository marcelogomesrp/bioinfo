from django.template import Library
import time

register = Library()

@register.filter()
def seconds_to_time(value):
    v = int(value)
    seconds = v % 60
    total_minutes = v / 60
    minutes = total_minutes % 60
    total_hours = total_minutes / 60
    return '%sh %sm %ss' % (total_hours, minutes, seconds)