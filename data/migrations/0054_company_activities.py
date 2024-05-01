# Generated by Django 5.0.4 on 2024-04-16 14:05

import data.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0053_merge_20240415_1856"),
    ]

    operations = [
        migrations.AddField(
            model_name="company",
            name="activities",
            field=data.fields.MultipleChoiceField(
                base_field=models.CharField(
                    choices=[
                        ("FABRICANT", "Fabricant"),
                        ("FAÇONNIER", "Façonnier"),
                        ("IMPORTATEUR", "Importateur"),
                        ("INTRODUCTEUR", "Introducteur"),
                        ("CONSEIL", "Conseil"),
                        ("DISTRIBUTEUR", "Distributeur"),
                    ]
                ),
                default=list,
                size=None,
                verbose_name="activités",
            ),
        ),
    ]