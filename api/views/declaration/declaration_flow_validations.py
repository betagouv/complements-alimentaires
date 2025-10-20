from data.choices import AuthorizationModes
from data.models import Attachment, Declaration

# Les validateurs dans ce fichier retournent une tuple avec les `field_errors` et les
# `non_field_errors` pour une déclaration.


def validate_mandatory_fields(declaration) -> tuple[list, list]:
    field_errors = []
    non_field_errors = []

    # Les champs obligatoires du produit pour passer en instruction sont remplis
    mandatory_product_fields = [
        "company",
        "name",
        "galenic_formulation",
        "populations",
        "effects",
        "daily_recommended_dose",
        "minimum_duration",
        "conditions_not_recommended",
        "address",
        "postal_code",
        "city",
        "country",
        "unit_quantity",
        "unit_measurement",
    ]
    missing_product_fields = [field for field in mandatory_product_fields if not getattr(declaration, field)]
    field_errors += [
        {field: f"« {Declaration._meta.get_field(field).verbose_name} » ne peut pas être vide"}
        for field in missing_product_fields
    ]
    has_label = declaration.attachments.filter(type=Attachment.AttachmentType.LABEL).exists()
    if not has_label:
        field_errors.append({"attachments": "La demande doit contenir au moins une pièce jointe de l'étiquetage"})

    plants = list(declaration.declared_plants.all())
    microorganisms = list(declaration.declared_microorganisms.all())
    ingredients = list(declaration.declared_ingredients.all())
    substances = list(declaration.declared_substances.all())

    all_ingredients = [] + plants + microorganisms + substances + ingredients
    new_ingredients = [x for x in all_ingredients if x.new]
    new_eu_ingredients = [x for x in new_ingredients if x.authorization_mode == AuthorizationModes.EU]
    if any(new_eu_ingredients) and not declaration.attachments.exclude(type=Attachment.AttachmentType.LABEL).exists():
        field_errors.append(
            {
                "attachments": "La demande doit contenir la pièce jointe du texte qui permette de justifier de l’application du principe de reconnaissance mutuelle"
            }
        )

    for new_ingredient in new_ingredients:
        if not new_ingredient.authorization_mode:
            field_errors.append(
                {
                    "authorization_mode": "Merci de renseigner le mode d'autorisation de l'ingrédient "
                    + new_ingredient.new_name
                }
            )

    for new_eu_ingredient in new_eu_ingredients:
        if not new_eu_ingredient.eu_reference_country:
            field_errors.append(
                {
                    "eu_reference_country": "Merci de renseigner le pays de référence de l'ingrédient "
                    + new_eu_ingredient.new_name
                }
            )
        if not new_eu_ingredient.eu_legal_source:
            field_errors.append(
                {
                    "eu_legal_source": "Merci de renseigner la source réglementaire de l'ingrédient "
                    + new_eu_ingredient.new_name
                }
            )
    for declared_plant in plants:
        if not declared_plant_is_complete(declared_plant):
            non_field_errors += ["Merci de renseigner les informations manquantes des plantes ajoutées"]

    for declared_microorganism in microorganisms:
        if not declared_microorganism_is_complete(declared_microorganism):
            non_field_errors += ["Merci de renseigner les informations manquantes des micro-organismes ajoutées"]

    for computed_substance in declaration.computed_substances.all():
        if not computed_substance_is_complete(computed_substance):
            non_field_errors += ["Merci de renseigner les informations manquantes dans le tableau des substances"]
    return (field_errors, non_field_errors)


def declared_plant_is_complete(plant):
    if not plant.active:
        return plant.used_part and plant.quantity and plant.unit
    return plant.used_part and plant.quantity and plant.unit and plant.preparation


def declared_microorganism_is_complete(mo):
    if not mo.active:
        return True
    return mo.strain and (not mo.activated or mo.quantity)


def computed_substance_is_complete(computed_substance):
    return computed_substance.quantity is not None if computed_substance.substance.must_specify_quantity else True


def validate_number_of_elements(declaration) -> tuple[list, list]:
    non_field_errors = []
    has_elements = (
        declaration.declared_plants.exists()
        or declaration.declared_microorganisms.exists()
        or declaration.declared_ingredients.exists()
        or declaration.declared_substances.exists()
    )
    if not has_elements:
        non_field_errors += ["Le complément doit comporter au moins un ingrédient"]
    return ([], non_field_errors)
