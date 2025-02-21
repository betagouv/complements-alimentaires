# Generated by Django 5.1.5 on 2025-02-20 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0120_declaration_teleicare_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declaration',
            name='calculated_article',
            field=models.TextField(blank=True, choices=[('ART_15', 'Article 15'), ('ART_15_WARNING', 'Article 15 Vigilance'), ('ART_15_HIGH_RISK_POPULATION', 'Article 15 Population à risque'), ('ART_16', 'Article 16'), ('ART_18', 'Article 18'), ('ANSES_REFERAL', 'nécessite saisine ANSES')], verbose_name='article calculé automatiquement'),
        ),
        migrations.AlterField(
            model_name='declaration',
            name='overridden_article',
            field=models.TextField(blank=True, choices=[('ART_15', 'Article 15'), ('ART_15_WARNING', 'Article 15 Vigilance'), ('ART_15_HIGH_RISK_POPULATION', 'Article 15 Population à risque'), ('ART_16', 'Article 16'), ('ART_18', 'Article 18'), ('ANSES_REFERAL', 'nécessite saisine ANSES')], verbose_name='article manuellement spécifié'),
        ),
        migrations.AlterField(
            model_name='historicaldeclaration',
            name='calculated_article',
            field=models.TextField(blank=True, choices=[('ART_15', 'Article 15'), ('ART_15_WARNING', 'Article 15 Vigilance'), ('ART_15_HIGH_RISK_POPULATION', 'Article 15 Population à risque'), ('ART_16', 'Article 16'), ('ART_18', 'Article 18'), ('ANSES_REFERAL', 'nécessite saisine ANSES')], verbose_name='article calculé automatiquement'),
        ),
        migrations.AlterField(
            model_name='historicaldeclaration',
            name='overridden_article',
            field=models.TextField(blank=True, choices=[('ART_15', 'Article 15'), ('ART_15_WARNING', 'Article 15 Vigilance'), ('ART_15_HIGH_RISK_POPULATION', 'Article 15 Population à risque'), ('ART_16', 'Article 16'), ('ART_18', 'Article 18'), ('ANSES_REFERAL', 'nécessite saisine ANSES')], verbose_name='article manuellement spécifié'),
        ),
    ]
