# Generated by Django 5.1.7 on 2025-03-20 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0128_remove_historicalsubstance_ca_max_quantity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalsubstance',
            name='ca_max_quantity',
        ),
        migrations.RemoveField(
            model_name='historicalsubstance',
            name='siccrf_max_quantity',
        ),
        migrations.RemoveField(
            model_name='substance',
            name='ca_max_quantity',
        ),
        migrations.RemoveField(
            model_name='substance',
            name='siccrf_max_quantity',
        ),
    ]
