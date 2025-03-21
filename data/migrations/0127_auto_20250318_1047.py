# Generated by Django 5.1.7 on 2025-03-18 09:47

from django.db import migrations
from data.etl.teleicare_history.extractor import get_oldest_and_latest
from data.models.teleicare_history.ica_declaration import IcaDeclaration, IcaVersionDeclaration

class Migration(migrations.Migration):

    dependencies = [
        ('data', '0126_icaingredient_icaingredientautre_icamicroorganisme_and_more'),
    ]
    
    def set_unit_quantity_and_daily_recommended_dose(apps, schema_editor):
        """Set action to the first snapshot of declarations from TeleIcare"""
        # Ce code a été exécuté dans le django shell pour éviter un freeze du deployement
        # Declaration = apps.get_model("data", "Declaration")
        # for declaration in Declaration.objects.exclude(siccrf_id=None).iterator():
        #     all_ica_declarations = IcaDeclaration.objects.filter(cplalim_id=declaration.siccrf_id)
        #     if all_ica_declarations.exists():
        #         _, latest_ica_declaration = get_oldest_and_latest(all_ica_declarations)
        #         declaration_versions = IcaVersionDeclaration.objects.filter(
        #             dcl_id=latest_ica_declaration.dcl_ident,
        #             stattdcl_ident__in=[
        #                 2,
        #                 5,
        #                 6,
        #                 8,
        #             ],  # status 'autorisé', 'refusé', 'arrêt commercialisation', 'abandonné'
        #             stadcl_ident=8,  # état 'clos'
        #         )
        #         latest_ica_version_declaration = declaration_versions.order_by("vrsdecl_numero").last()
        #         declaration.unit_quantity = declaration.daily_recommended_dose # FloatField to FloatField
        #         declaration.daily_recommended_dose = latest_ica_version_declaration.vrsdecl_djr #TextField to TextField
        #         declaration.save()
        pass

    def reverse_set_unit_quantity_and_daily_recommended_dose(apps, schema_editor):
        pass

    operations = [
        migrations.RunPython(set_unit_quantity_and_daily_recommended_dose, reverse_set_unit_quantity_and_daily_recommended_dose),

    ]
