# Generated by Django 5.1.7 on 2025-05-14 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0147_alter_historicalpopulation_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(blank=True, choices=[('LABEL', 'Étiquetage'), ('REGULATORY_PROOF', 'Preuve règlementaire'), ('CERTIFICATE_AUTHORITY', "Attestation d'une autorité compétente"), ('SPEC_SHEET', 'Fiche technique'), ('ADDITIONAL_INFO', 'Compléments info professionnel'), ('OBSERVATIONS', 'Observations professionnel'), ('PROFESSIONAL_MAIL', 'Autre courrier du professionnel'), ('DRAFT', 'Brouillon'), ('OTHER', 'Autre professionnel'), ('ANALYSIS_REPORT', "Bulletin d'analyse")], max_length=50, null=True, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='historicalattachment',
            name='type',
            field=models.CharField(blank=True, choices=[('LABEL', 'Étiquetage'), ('REGULATORY_PROOF', 'Preuve règlementaire'), ('CERTIFICATE_AUTHORITY', "Attestation d'une autorité compétente"), ('SPEC_SHEET', 'Fiche technique'), ('ADDITIONAL_INFO', 'Compléments info professionnel'), ('OBSERVATIONS', 'Observations professionnel'), ('PROFESSIONAL_MAIL', 'Autre courrier du professionnel'), ('DRAFT', 'Brouillon'), ('OTHER', 'Autre professionnel'), ('ANALYSIS_REPORT', "Bulletin d'analyse")], max_length=50, null=True, verbose_name='type'),
        ),
    ]
