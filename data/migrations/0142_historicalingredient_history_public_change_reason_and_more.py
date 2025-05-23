# Generated by Django 5.1.7 on 2025-04-29 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0141_merge_20250429_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalingredient',
            name='history_public_change_reason',
            field=models.CharField(blank=True, max_length=100, verbose_name='Raison de changement (public)'),
        ),
        migrations.AddField(
            model_name='historicalmicroorganism',
            name='history_public_change_reason',
            field=models.CharField(blank=True, max_length=100, verbose_name='Raison de changement (public)'),
        ),
        migrations.AddField(
            model_name='historicalplant',
            name='history_public_change_reason',
            field=models.CharField(blank=True, max_length=100, verbose_name='Raison de changement (public)'),
        ),
        migrations.AddField(
            model_name='historicalsubstance',
            name='history_public_change_reason',
            field=models.CharField(blank=True, max_length=100, verbose_name='Raison de changement (public)'),
        ),
    ]
