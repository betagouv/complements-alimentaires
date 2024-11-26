# Generated by Django 5.1.3 on 2024-11-26 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0105_alter_declaration_calculated_article_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="calculated_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_15_HIGH_RISK_POPULATION", "Article 15 Population à risque"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article calculé automatiquement",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="overriden_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_15_HIGH_RISK_POPULATION", "Article 15 Population à risque"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="calculated_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_15_HIGH_RISK_POPULATION", "Article 15 Population à risque"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article calculé automatiquement",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="overriden_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_15_HIGH_RISK_POPULATION", "Article 15 Population à risque"),
                    ("ART_16", "Article 16"),
                    ("ANSES_REFERAL", "nécessite saisine ANSES"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
    ]
