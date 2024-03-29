# Generated by Django 5.0.2 on 2024-03-07 13:19

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0023_alter_user_options_alter_user_is_active"),
    ]

    operations = [
        migrations.CreateModel(
            name="CompanySupervisor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "gestionnaire d'entreprise",
                "verbose_name_plural": "gestionnaires d'entreprise",
            },
        ),
        migrations.CreateModel(
            name="Company",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("social_name", models.CharField(verbose_name="dénomination sociale")),
                (
                    "commercial_name",
                    models.CharField(
                        help_text="nom commercial", verbose_name="enseigne"
                    ),
                ),
                (
                    "siret",
                    models.CharField(
                        help_text="14 chiffres",
                        validators=[
                            django.core.validators.MinLengthValidator(14),
                            django.core.validators.MaxLengthValidator(14),
                        ],
                        verbose_name="n° SIRET",
                    ),
                ),
                (
                    "supervisor",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="data.companysupervisor",
                        verbose_name="gestionnaire d'entreprise",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Declarant",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="utilisateur",
                    ),
                ),
            ],
            options={
                "verbose_name": "déclarant",
            },
        ),
    ]
