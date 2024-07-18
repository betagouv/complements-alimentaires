# Generated by Django 5.0.7 on 2024-07-18 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0077_alter_snapshot_action"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="conditioning",
            field=models.TextField(blank=True, verbose_name="conditionnements"),
        ),
        migrations.AlterField(
            model_name="declaration",
            name="post_validation_status",
            field=models.CharField(
                blank=True,
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status à assigner après la validation",
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="post_validation_status",
            field=models.CharField(
                blank=True,
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status à assigner après la validation",
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="snapshot",
            name="post_validation_status",
            field=models.CharField(
                blank=True,
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="status à assigner après la validation",
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
                    ("WITHDRAWN", "Retiré du marché"),
                ],
                max_length=50,
                verbose_name="status",
            ),
        ),
    ]
