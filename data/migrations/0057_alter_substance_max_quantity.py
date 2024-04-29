# Generated by Django 5.0.4 on 2024-04-22 10:15

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0056_alter_substance_max_quantity_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="substance", name="max_quantity"),
        migrations.AddField(
            model_name="substance",
            name="max_quantity",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.F("ca_max_quantity"), models.F("siccrf_max_quantity")
                ),
                output_field=models.FloatField(blank=True, null=True, verbose_name="quantité maximale autorisée"),
            ),
        ),
    ]