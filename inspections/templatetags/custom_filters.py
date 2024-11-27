from django import template

register = template.Library()

@register.filter
def split(value, delimiter):
    """
    Splits the input string by the given delimiter.
    """
    if not isinstance(value, str):
        return value
    return value.split(delimiter)