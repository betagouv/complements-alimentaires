from django.db import models 
from django.db.models.functions import Coalesce

from .mixins import WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean, WithSICCRFDefaultFields, WithCADefaultFields


class CommonModelManager(models.Manager):
    """
    Annotates with `is_obsolete` and `name` to emulate filtering by property
    """
    def get_queryset(self):
        # add a `is_obsolete` annotation (with fallback) to the initial queryset
        return super(CommonModelManager, self).get_queryset().annotate(is_obsolete=Coalesce('siccrf_is_obsolete', 'CA_is_obsolete')).annotate(name=Coalesce('siccrf_name', 'CA_name'))


class CommonModel(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean, WithSICCRFDefaultFields, WithCADefaultFields):
    """
    Les modèles ingrédients et les synonymes héritent de ce modèle
    """
    class Meta:
        abstract = True

    objects = CommonModelManager()

    def __str__(self):
        return self.name

    @property
    def object_type(self):
        return self.__class__.__name__.lower()

    # D'autres champs sont présents dans les CSV d'ingredients mais actuellement non importés
    # fctingr = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # stingsbs = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # taing = models.IntegerField() -> ingredient
