from data.models import Declaration

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
    return (field_errors, non_field_errors)


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
