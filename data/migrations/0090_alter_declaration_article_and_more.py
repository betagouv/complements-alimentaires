# Generated by Django 5.1 on 2024-08-29 08:00

import django.db.models.functions.comparison
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0089_declaration_calculated_article_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="article",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.Case(
                        models.When(overriden_article="", then=models.Value(None)),
                        default="overriden_article",
                    ),
                    models.Case(
                        models.When(calculated_article="", then=models.Value(None)),
                        default="calculated_article",
                    ),
                    models.Value(None),
                ),
                output_field=models.TextField(null=True, verbose_name="article"),
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="calculated_article",
            field=models.TextField(
                blank=True,
                choices=[
                    ("ART_15", "Article 15"),
                    ("ART_15_WARNING", "Article 15 Vigilance"),
                    ("ART_16", "Article 16"),
                    ("ART_17", "Article 17"),
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
                    ("ART_16", "Article 16"),
                    ("ART_17", "Article 17"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="article",
            field=models.GeneratedField(
                db_persist=True,
                expression=django.db.models.functions.comparison.Coalesce(
                    models.Case(
                        models.When(overriden_article="", then=models.Value(None)),
                        default="overriden_article",
                    ),
                    models.Case(
                        models.When(calculated_article="", then=models.Value(None)),
                        default="calculated_article",
                    ),
                    models.Value(None),
                ),
                output_field=models.TextField(null=True, verbose_name="article"),
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
                    ("ART_16", "Article 16"),
                    ("ART_17", "Article 17"),
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
                    ("ART_16", "Article 16"),
                    ("ART_17", "Article 17"),
                ],
                verbose_name="article manuellement spécifié",
            ),
        ),
    ]
