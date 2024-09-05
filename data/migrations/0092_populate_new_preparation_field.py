# Generated by Django 5.1 on 2024-09-05 12:34
# Ecrite à la main

from django.db import migrations


def replace_textfield_by_foreign_key(apps, schema_editor):
    Preparation = apps.get_model('data', 'Preparation')
    DeclaredPlant = apps.get_model('data', 'DeclaredPlant')
    for dPlant in DeclaredPlant.objects.all():
        preparation = Preparation.objects.get(name=dPlant.preparation_old)
        dPlant.preparation = preparation
        dPlant.save()


def reverse_replace(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0091_declaredplant_preparation_old_and_more"),
    ]

    operations = [
        migrations.RunPython(replace_textfield_by_foreign_key, reverse_replace),

    ]
