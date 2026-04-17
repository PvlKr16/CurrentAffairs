from django import template
import os

register = template.Library()


@register.filter
def filename(value):
    return os.path.basename(value.name)


@register.filter
def ext(value):
    return os.path.splitext(value.name)[1].lower()
