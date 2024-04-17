def has_mandatory_fields_for_submission(declaration):
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
        {field: "Ce champ est nécessaire pour passer la déclaration à l'étape d'instruction"}
        for field in missing_product_fields
    ]
    return (field_errors, non_field_errors)


def has_elements(declaration):
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
