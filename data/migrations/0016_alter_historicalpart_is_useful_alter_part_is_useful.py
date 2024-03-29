# Generated by Django 5.0.2 on 2024-02-13 10:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0015_remove_usefulpart_plant_remove_usefulpart_plantpart_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalpart",
            name="is_useful",
            field=models.BooleanField(
                default=False, verbose_name="🍵 utile (selon la base SICCRF) ?"
            ),
        ),
        migrations.AlterField(
            model_name="part",
            name="is_useful",
            field=models.BooleanField(
                default=False, verbose_name="🍵 utile (selon la base SICCRF) ?"
            ),
        ),
    ]
