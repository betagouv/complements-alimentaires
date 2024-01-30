# Generated by Django 5.0.1 on 2024-01-24 10:57

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "data",
            "0013_rename_historicalusefulpartrelation_historicalusefulpart_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="condition",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalcondition",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalingredient",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalingredientsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalmicroorganism",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalmicroorganismsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalplant",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalplantfamily",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalplantpart",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalplantsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalpopulation",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalsubstance",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="historicalsubstancesynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="ingredientsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="microorganism",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="microorganismsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="plant",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="plantfamily",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="plantpart",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="plantsynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="population",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="substance",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
        migrations.AddField(
            model_name="substancesynonym",
            name="missing_import_data",
            field=models.BooleanField(
                blank=True, default=False, editable=False, null=True
            ),
        ),
    ]
