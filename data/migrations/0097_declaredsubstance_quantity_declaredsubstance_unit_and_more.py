# Generated by Django 5.1.1 on 2024-09-24 14:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0096_remove_historicalsubstance_substance_types_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="declaredsubstance",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR"
            ),
        ),
        migrations.AddField(
            model_name="declaredsubstance",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="data.substanceunit",
                verbose_name="unité",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredsubstance",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR"
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredsubstance",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="data.substanceunit",
                verbose_name="unité",
            ),
        ),
    ]
