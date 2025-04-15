import logging

from django.db import migrations

import pandas as pd
from django.db.models import TextField, Transform

from data.models.substance import SubstanceType

logger = logging.getLogger(__name__)

TELEICARE_SUBSTANCE_TYPE_MAPPING = {
    1: SubstanceType.VITAMIN,
    2: SubstanceType.MINERAL,
    3: SubstanceType.BIOACTIVE_SUBSTANCE,
    # 4: Ingrédient actif (sans substance active) -> Substance à supprimer, c'est un ingrédient
    5: SubstanceType.SECONDARY_METABOLITE,
    # 6: Autre substance active -> Pas de type spécifique
}


class LowerValue(Transform):
    lookup_name = "lower"
    function = "LOWER"


TextField.register_lookup(LowerValue)


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0135_alter_substance_substance_types"),
    ]

    def set_substance_types_from_teleicare(apps, schema_editor):
        """Ajout des types de substances TeleIcare aux substances"""
        # Cette migration est appliquée manuellement dans le shell django en staging, prod, demo
        Substance = apps.get_model("data", "Substance")
        Ingredient = apps.get_model("data", "Ingredient")
        siccrf_substances = pd.read_csv("data/migrations/0136_REF_ICA_SUBSTANCE_ACTIVE_TYPES.csv", sep=",")
        siccrf_substances[["SBSACT_IDENT", "TYSUBST_IDENT", "SBSACT_LIBELLE"]]

        for index, siccrf_substance in siccrf_substances.iterrows():
            ca_substance = Substance.objects.get(siccrf_id=siccrf_substance["SBSACT_IDENT"])

            if siccrf_substance["TYSUBST_IDENT"] == 4:
                # cette substance n'en est pas une mais un Ingrédient actif
                ca_substance.ca_is_obsolete = True
                same_ingredient = Ingredient.objects.filter(name__lower=siccrf_substance["SBSACT_LIBELLE"].lower())
                if not same_ingredient.exists():
                    logger.info(
                        f"Création de l'ingrédient actif {siccrf_substance['SBSACT_LIBELLE']} correspondant à Substance.siccrf_id={siccrf_substance['SBSACT_IDENT']} nécessaire."
                    )
            elif siccrf_substance["TYSUBST_IDENT"] == 6:
                # si type = 6, alors c'est le default substance_types = []
                pass
            else:
                ca_substance.substance_types.append(TELEICARE_SUBSTANCE_TYPE_MAPPING[siccrf_substance["TYSUBST_IDENT"]])
                ca_substance.substance_types = list(set(ca_substance.substance_types))

            ca_substance.save()

    def reverse_set_substance_types_from_teleicare(apps, schema_editor):
        pass

    operations = [
        migrations.RunPython(set_substance_types_from_teleicare, reverse_set_substance_types_from_teleicare),
    ]
