from django import template
from django.utils.translation import gettext as _

register = template.Library()

@register.filter
def t(value):
    return _(value)