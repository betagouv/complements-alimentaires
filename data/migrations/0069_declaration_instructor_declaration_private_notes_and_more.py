# Generated by Django 5.0.4 on 2024-06-12 14:25

import data.models.snapshot
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0068_alter_ingredient_status_alter_microorganism_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="declaration",
            name="instructor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="declarations",
                to="data.instructionrole",
                verbose_name="instructeur",
            ),
        ),
        migrations.AddField(
            model_name="declaration",
            name="private_notes",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="notes à destination de l'administration",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="instructor",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="data.instructionrole",
                verbose_name="instructeur",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaration",
            name="private_notes",
            field=models.TextField(
                blank=True,
                default="",
                verbose_name="notes à destination de l'administration",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="author",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="declarations",
                to=settings.AUTH_USER_MODEL,
                verbose_name="auteur",
            ),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="conditions_not_recommended",
            field=models.ManyToManyField(
                blank=True,
                to="data.condition",
                verbose_name="consommation déconseillée",
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
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
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
                    ("OBSERVATION", "En observation"),
                    ("ABANDONED", "Abandonnée"),
                    ("AUTHORIZED", "Autorisée"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.CreateModel(
            name="Snapshot",
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
                ("creation_date", models.DateTimeField(auto_now_add=True)),
                ("modification_date", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("DRAFT", "Brouillon"),
                            ("AWAITING_INSTRUCTION", "En attente d'instruction"),
                            ("ONGOING_INSTRUCTION", "Instruction en cours"),
                            ("OBSERVATION", "En observation"),
                            ("ABANDONED", "Abandonnée"),
                            ("AUTHORIZED", "Autorisée"),
                        ],
                        max_length=50,
                        verbose_name="status",
                    ),
                ),
                (
                    "expiration_days",
                    models.IntegerField(
                        blank=True, null=True, verbose_name="délai de réponse"
                    ),
                ),
                (
                    "json_declaration",
                    models.JSONField(
                        encoder=data.models.snapshot.CustomJSONEncoder,
                        verbose_name="données au moment de la création",
                    ),
                ),
                (
                    "comment",
                    models.TextField(
                        blank=True, default="", verbose_name="commentaire"
                    ),
                ),
                (
                    "declaration",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="snapshots",
                        to="data.declaration",
                        verbose_name="déclaration",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="snapshots",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="personne ayant effectué le changement",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]