# Generated by Django 5.0.6 on 2024-06-06 08:43
# Modifié manuellement pour que les anciens champs `status` soient transformés en `siccrf_status`

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0068_alter_ingredient_status_alter_microorganism_status_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ingredient",
            old_name="status",
            new_name="siccrf_status",
        ),
        migrations.RenameField(
            model_name="microorganism",
            old_name="status",
            new_name="siccrf_status",
        ),
        migrations.RenameField(
            model_name="plant",
            old_name="status",
            new_name="siccrf_status",
        ),
        migrations.RenameField(
            model_name="substance",
            old_name="status",
            new_name="siccrf_status",
        ),
        migrations.AddField(
            model_name="historicalingredient",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="historicalmicroorganism",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="historicalplant",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="historicalsubstance",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="microorganism",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="plant",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AddField(
            model_name="substance",
            name="ca_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon Compl'Alim",
            ),
        ),
        migrations.AlterField(
            model_name="condition",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="effect",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="galenicformulation",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalcondition",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicaleffect",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalgalenicformulation",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalingredient",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalplant",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalplantfamily",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalplantpart",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalpopulation",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="historicalsubstance",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="ingredient",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("siccrf_status"),
                    models.F("ca_status"),
                ),
                output_field=models.IntegerField(
                    verbose_name="statut de l'ingrédient ou substance",
                    choices=[(1, "autorisé"), (2, "non autorisé")],
                    null=True,
                ),
            ),
        ),
        migrations.AddField(
            model_name="microorganism",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("siccrf_status"),
                    models.F("ca_status"),
                ),
                output_field=models.IntegerField(
                    verbose_name="statut de l'ingrédient ou substance",
                    choices=[(1, "autorisé"), (2, "non autorisé")],
                    null=True,
                ),
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AddField(
            model_name="plant",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("siccrf_status"),
                    models.F("ca_status"),
                ),
                output_field=models.IntegerField(
                    verbose_name="statut de l'ingrédient ou substance",
                    choices=[(1, "autorisé"), (2, "non autorisé")],
                    null=True,
                ),
            ),
        ),
        migrations.AlterField(
            model_name="plantfamily",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="plantpart",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="population",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AlterField(
            model_name="substance",
            name="ca_name",
            field=models.TextField(blank=True, verbose_name="nom CA"),
        ),
        migrations.AddField(
            model_name="substance",
            name="status",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("siccrf_status"),
                    models.F("ca_status"),
                ),
                output_field=models.IntegerField(
                    verbose_name="statut de l'ingrédient ou substance",
                    choices=[(1, "autorisé"), (2, "non autorisé")],
                    null=True,
                ),
            ),
        ),
    ]
