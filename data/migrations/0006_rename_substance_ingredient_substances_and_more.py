# Generated by Django 4.2.7 on 2023-12-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0005_family_ingredient_microorganism_plant_plantpart_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="ingredient",
            old_name="substance",
            new_name="substances",
        ),
        migrations.RenameField(
            model_name="microorganism",
            old_name="substance",
            new_name="substances",
        ),
        migrations.RenameField(
            model_name="plant",
            old_name="substance",
            new_name="substances",
        ),
        migrations.AlterField(
            model_name="substance",
            name="max_quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité maximale autorisée"
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="min_quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité minimale autorisée"
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="must_specify_quantity",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="substance",
            name="nutritional_reference",
            field=models.FloatField(
                blank=True, null=True, verbose_name="apport nutritionnel conseillé"
            ),
        ),
    ]
