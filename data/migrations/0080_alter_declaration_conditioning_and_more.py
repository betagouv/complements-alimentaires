# Generated by Django 5.0.7 on 2024-07-30 08:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0079_snapshot_blocking_reasons"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="conditioning",
            field=models.TextField(blank=True, verbose_name="conditionnement"),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="populations",
            field=models.ManyToManyField(
                blank=True, to="data.population", verbose_name="populations cibles"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="conditioning",
            field=models.TextField(blank=True, verbose_name="conditionnement"),
        ),
    ]
