# Generated by Django 4.2.7 on 2023-12-11 08:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0003_blogpost"),
    ]

    operations = [
        migrations.CreateModel(
            name="Condition",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("modification_date", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                ("name_en", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "condition de santé / facteurs de risque",
            },
        ),
        migrations.CreateModel(
            name="Population",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("modification_date", models.DateTimeField(auto_now=True)),
                ("name", models.TextField()),
                ("name_en", models.TextField(blank=True)),
            ],
            options={
                "verbose_name": "Population cible / à risque",
            },
        ),
        migrations.RemoveField(
            model_name="historicalingredient",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalmicroorganism",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalplant",
            name="history_user",
        ),
        migrations.RemoveField(
            model_name="historicalsubstance",
            name="history_user",
        ),
        migrations.DeleteModel(
            name="Ingredient",
        ),
        migrations.DeleteModel(
            name="Microorganism",
        ),
        migrations.DeleteModel(
            name="Plant",
        ),
        migrations.DeleteModel(
            name="Substance",
        ),
        migrations.DeleteModel(
            name="HistoricalIngredient",
        ),
        migrations.DeleteModel(
            name="HistoricalMicroorganism",
        ),
        migrations.DeleteModel(
            name="HistoricalPlant",
        ),
        migrations.DeleteModel(
            name="HistoricalSubstance",
        ),
    ]
