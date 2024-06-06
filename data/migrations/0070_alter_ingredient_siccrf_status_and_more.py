# Generated by Django 5.0.6 on 2024-06-06 10:00

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0069_historicalingredient_ca_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="siccrf_status",
            field=models.IntegerField(
                blank=True,
                choices=[(1, "autorisé"), (2, "non autorisé")],
                default=None,
                null=True,
                verbose_name="statut de l'ingrédient ou substance selon TeleIcare",
            ),
        ),
    ]
