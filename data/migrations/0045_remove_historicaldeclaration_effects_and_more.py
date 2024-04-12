# Generated by Django 5.0.3 on 2024-04-08 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0044_effect_historicaleffect"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="historicaldeclaration",
            name="effects",
        ),
        migrations.RemoveField(
            model_name="declaration",
            name="effects",
        ),
        migrations.AddField(
            model_name="declaration",
            name="effects",
            field=models.ManyToManyField(
                blank=True,
                null=True,
                to="data.effect",
                verbose_name="objectifs ou effets",
            ),
        ),
    ]