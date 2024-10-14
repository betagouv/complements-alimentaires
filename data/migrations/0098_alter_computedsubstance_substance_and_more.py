# Generated by Django 5.1.1 on 2024-10-11 16:02
# Modifié manuellement pour :
# * remplir le champ DeclaredSubstance.unit à partir de DeclaredSubstance.substance.unit
# * modifier le champ calculated_article par ANSES_REFERAL si nécessaire

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0097_declaredsubstance_quantity_declaredsubstance_unit_and_more"),
    ]

    def set_unit(apps, schema_editor):
        """Set unit and recompute article (thanks to signal)"""
        DeclaredSubstance = apps.get_model("data", "DeclaredSubstance")
        ComputedSubstance = apps.get_model("data", "ComputedSubstance")
        Declaration = apps.get_model("data", "Declaration")
        for declared_substance in DeclaredSubstance.objects.all().iterator():
            if declared_substance.substance and declared_substance.quantity:
                declared_substance.unit = declared_substance.substance.unit
                declared_substance.save()

                if declared_substance.quantity and declared_substance.substance.max_quantity and declared_substance.quantity > declared_substance.substance.max_quantity:
                    declaration = Declaration.objects.get(id=declared_substance.declaration_id)
                    declaration.calculated_article = "ANSES_REFERAL"
                    declaration.save()
        for computed_substance in ComputedSubstance.objects.all().iterator():
            if computed_substance.substance and computed_substance.quantity:
                computed_substance.unit = computed_substance.substance.unit
                computed_substance.save()
                if computed_substance.quantity and computed_substance.substance.max_quantity and computed_substance.quantity > computed_substance.substance.max_quantity:
                    declaration = Declaration.objects.get(id=declared_substance.declaration_id)
                    declaration.calculated_article = "ANSES_REFERAL"
                    declaration.save()
                                    


    def reverse_set_unit(apps, schema_editor):
        pass

    operations = [
        migrations.AlterField(
            model_name="computedsubstance",
            name="substance",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="data.substance",
                verbose_name="substance ajoutée automatiquement car apportée par un ingrédient",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="calculated_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article calculé automatiquement",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="overriden_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcomputedsubstance",
            name="substance",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="data.substance",
                verbose_name="substance ajoutée automatiquement car apportée par un ingrédient",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="calculated_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article calculé automatiquement",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="overriden_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
        migrations.RunPython(set_unit, reverse_set_unit),

    ]
