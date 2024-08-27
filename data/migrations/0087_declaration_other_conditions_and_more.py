# Generated by Django 5.1 on 2024-08-22 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0086_alter_effect_options_alter_historicaleffect_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="declaration",
            name="other_conditions",
            field=models.TextField(
                blank=True,
                verbose_name="autres populations à risques ou facteurs de risques non listés",
            ),
        ),
        migrations.AddField(
            model_name="declaration",
            name="other_galenic_formulation",
            field=models.TextField(
                blank=True, verbose_name="autre forme galénique non listée"
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="other_conditions",
            field=models.TextField(
                blank=True,
                verbose_name="autres populations à risques ou facteurs de risques non listés",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="other_galenic_formulation",
            field=models.TextField(
                blank=True, verbose_name="autre forme galénique non listée"
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="other_effects",
            field=models.TextField(
                blank=True, verbose_name="autres objectifs ou effets non listés"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="other_effects",
            field=models.TextField(
                blank=True, verbose_name="autres objectifs ou effets non listés"
            ),
        ),
    ]
