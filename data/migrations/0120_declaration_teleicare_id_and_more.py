# Generated by Django 5.1.5 on 2025-01-30 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0119_merge_20250128_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaration',
            name='teleicare_id',
            field=models.TextField(blank=True, editable=False, null=True, unique=True, verbose_name='identifiant Teleicare connu par les déclarants et indiqué dans les attestations'),
        ),
        migrations.AddField(
            model_name='historicaldeclaration',
            name='teleicare_id',
            field=models.TextField(blank=True, db_index=True, editable=False, null=True, verbose_name='identifiant Teleicare connu par les déclarants et indiqué dans les attestations'),
        ),
    ]
