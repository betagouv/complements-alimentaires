# Generated by Django 5.0.3 on 2024-03-26 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0035_merge_20240326_1031"),
    ]

    operations = [
        migrations.AddField(
            model_name="declarant",
            name="companies",
            field=models.ManyToManyField(to="data.company", verbose_name="entreprises"),
        ),
    ]
