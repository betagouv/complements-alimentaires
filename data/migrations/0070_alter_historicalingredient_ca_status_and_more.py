# Generated by Django 5.0.6 on 2024-06-13 13:12

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0069_historicalingredient_ca_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalingredient",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="historicalmicroorganism",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="historicalplant",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="historicalsubstance",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_status"), models.F("siccrf_status")
                ),
                output_field=models.IntegerField(
                    choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                    null=True,
                    verbose_name="statut de l'ingrédient ou substance",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_status"), models.F("siccrf_status")
                ),
                output_field=models.IntegerField(
                    choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                    null=True,
                    verbose_name="statut de l'ingrédient ou substance",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_status"), models.F("siccrf_status")
                ),
                output_field=models.IntegerField(
                    choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                    null=True,
                    verbose_name="statut de l'ingrédient ou substance",
                ),
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_status"), models.F("siccrf_status")
                ),
                output_field=models.IntegerField(
                    choices=[(1, "autorisé"), (2, "non autorisé"), (3, "sans objet")],
                    null=True,
                    verbose_name="statut de l'ingrédient ou substance",
                ),
            ),
        ),
    ]
