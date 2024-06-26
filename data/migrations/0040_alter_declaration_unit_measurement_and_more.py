# Generated by Django 5.0.3 on 2024-04-03 08:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0039_declaration_computedsubstance_attachment_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="unit_measurement",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="data.substanceunit",
                verbose_name="unité de mesure pour une unité de consommation",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="unit_quantity",
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name="poids ou volume d'une unité de consommation",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="unit_quantity",
            field=models.FloatField(
                blank=True,
                null=True,
                verbose_name="poids ou volume d'une unité de consommation",
            ),
        ),
    ]
