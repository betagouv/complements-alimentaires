# Generated by Django 5.1.7 on 2025-05-07 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0143_fill_siccrf_registration_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='snapshot',
            name='effective_withdrawal_date',
            field=models.DateField(blank=True, null=True, verbose_name='date effective de retrait du marché'),
        ),
    ]
