from django import template

register = template.Library()


@register.filter
def pdf_safe(value):
    """Replace characters unsupported by the Marianne font used in PDF certificates."""
    if not isinstance(value, str):
        return value
    return value.replace("\u00b5", "u")  # µ (MICRO SIGN) → u
