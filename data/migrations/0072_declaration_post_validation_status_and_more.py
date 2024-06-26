# Generated by Django 5.0.6 on 2024-06-24 15:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0071_merge_20240617_0945"),
    ]

    operations = [
        migrations.AddField(
            model_name="declaration",
            name="post_validation_status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                    ("ONGOING_INSTRUCTION", "Instruction en cours"),
                    ("AWAITING_VISA", "En attente de visa"),
                    ("ONGOING_VISA", "Visa en cours"),
                    ("OBJECTION", "En objection"),
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                    ("REJECTED", "Refusée"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="post_validation_status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                    ("ONGOING_INSTRUCTION", "Instruction en cours"),
                    ("AWAITING_VISA", "En attente de visa"),
                    ("ONGOING_VISA", "Visa en cours"),
                    ("OBJECTION", "En objection"),
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                    ("REJECTED", "Refusée"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                    ("ONGOING_INSTRUCTION", "Instruction en cours"),
                    ("AWAITING_VISA", "En attente de visa"),
                    ("ONGOING_VISA", "Visa en cours"),
                    ("OBJECTION", "En objection"),
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                    ("REJECTED", "Refusée"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                    ("ONGOING_INSTRUCTION", "Instruction en cours"),
                    ("AWAITING_VISA", "En attente de visa"),
                    ("ONGOING_VISA", "Visa en cours"),
                    ("OBJECTION", "En objection"),
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                    ("REJECTED", "Refusée"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="snapshot",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                    ("ONGOING_INSTRUCTION", "Instruction en cours"),
                    ("AWAITING_VISA", "En attente de visa"),
                    ("ONGOING_VISA", "Visa en cours"),
                    ("OBJECTION", "En objection"),
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                    ("REJECTED", "Refusée"),
                ],
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.CreateModel(
            name="VisaRole",
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
                "verbose_name": "rôle de visa",
                "verbose_name_plural": "rôles de visa",
            },
        ),
        migrations.AddField(
            model_name="declaration",
            name="visor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="declarations",
                to="data.visarole",
                verbose_name="visor",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="visor",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="data.visarole",
                verbose_name="visor",
            ),
        ),
    ]
