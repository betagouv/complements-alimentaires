from .mixins import WithCreationAndModificationDate, WithMissingImportBoolean, WithDefaultFields


class CommonModel(WithCreationAndModificationDate, WithMissingImportBoolean, WithDefaultFields):
    """
    Les modèles ingrédients et les synonymes héritent de ce modèle
    """

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    @property
    def object_type(self):
        return self.__class__.__name__.lower()

    # D'autres champs sont présents dans les CSV d'ingredients mais actuellement non importés
    # fctingr = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # stingsbs = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # taing = models.IntegerField() -> ingredient
