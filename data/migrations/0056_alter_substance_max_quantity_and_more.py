# Generated by Django 5.0.4 on 2024-04-22 09:56

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0055_plant_family_by_id_alter_plant_family"),
    ]

    operations = [
        migrations.AlterField(
            model_name="substance",
            name="max_quantity",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_nutritional_reference"),
                    models.F("siccrf_nutritional_reference"),
                ),
                output_field=models.FloatField(
                    blank=True, null=True, verbose_name="quantité maximale autorisée"
                ),
            ),
        ),
        migrations.AlterField(
            model_name="substanceunit",
            name="name",
            field=models.CharField(max_length=3, verbose_name="unité"),
        ),
    ]
