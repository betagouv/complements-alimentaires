# Generated by Django 5.1.7 on 2025-06-24 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0157_controlrole'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaredplant',
            name='is_part_request',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicaldeclaredplant',
            name='is_part_request',
            field=models.BooleanField(default=False),
        ),
    ]
