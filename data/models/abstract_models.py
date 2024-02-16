from .mixins import WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean, WithSICCRFDefaultFields


class SICCRFCommonModel(WithCreationAndModificationDate, WithHistory, WithMissingImportBoolean, WithSICCRFDefaultFields):
    """
    Les modèles ingrédients et les synonymes héritent de ce modèle
    """
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    # D'autres champs sont présents dans les CSV d'ingredients mais actuellement non importés
    # fctingr = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # stingsbs = models.IntegerField() -> substance, ingredient, plante, micro-organisme
    # taing = models.IntegerField() -> ingredient
