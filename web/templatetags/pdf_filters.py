from django import template

register = template.Library()


@register.filter
def pdf_safe(value):
    """
    Remplace le « µ » pour un « u » dans les PDF car la police Marianne n'a pas
    le caractère nécessaire
    """
    if not isinstance(value, str):
        return value
    return value.replace("\u00b5", "u")
