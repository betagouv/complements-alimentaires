# Generated by Django 5.0.7 on 2024-08-01 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0080_alter_declaration_conditioning_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="declaredingredient",
            name="new_type",
            field=models.TextField(blank=True, verbose_name="type de l'ingrédient"),
        ),
        migrations.AddField(
            model_name="historicaldeclaredingredient",
            name="new_type",
            field=models.TextField(blank=True, verbose_name="type de l'ingrédient"),
        ),
    ]