# Generated by Django 5.1.2 on 2024-11-07 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0100_declaration_private_notes_visa_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="galenicformulation",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalgalenicformulation",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalingredient",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalmicroorganism",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalplant",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="historicalpreparation",
            name="contains_alcohol",
            field=models.BooleanField(
                default=False, verbose_name="la préparation contient-elle de l'alcool ?"
            ),
        ),
        migrations.AddField(
            model_name="historicalsubstance",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="ingredient",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="microorganism",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="plant",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
        migrations.AddField(
            model_name="preparation",
            name="contains_alcohol",
            field=models.BooleanField(
                default=False, verbose_name="la préparation contient-elle de l'alcool ?"
            ),
        ),
        migrations.AddField(
            model_name="substance",
            name="is_risky",
            field=models.BooleanField(
                default=False,
                verbose_name="nécessite une instruction manuelle et vigilante ?",
            ),
        ),
    ]
