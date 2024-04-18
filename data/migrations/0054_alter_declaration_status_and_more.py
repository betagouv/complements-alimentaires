# Generated by Django 5.0.4 on 2024-04-18 12:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0053_merge_20240415_1856"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente de retour instruction"),
                    ("AWAITING_PRODUCER", "En attente de retour du déclarant"),
                    ("REJECTED", "Rejeté"),
                    ("APPROVED", "Validé"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="status",
            field=models.CharField(
                choices=[
                    ("DRAFT", "Brouillon"),
                    ("AWAITING_INSTRUCTION", "En attente de retour instruction"),
                    ("AWAITING_PRODUCER", "En attente de retour du déclarant"),
                    ("REJECTED", "Rejeté"),
                    ("APPROVED", "Validé"),
                ],
                default="DRAFT",
                max_length=50,
                verbose_name="Status",
            ),
        ),
    ]
