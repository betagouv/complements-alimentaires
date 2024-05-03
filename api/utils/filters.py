import django_filters


class BaseNumberInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    """
    Ce filtre permet d'effectuer des recherches par plusieurs chiffres avec la virgule comme
    séparateur. Pratique pour le filtrage d'IDs des modèles.

    Par exemple, dans un URL on pourrait avoir `company=12,13,14` pour filtrer des objets ayant
    comme compagnie une de ces trois (IDs 12, 13 ou 14).
    """

    pass
