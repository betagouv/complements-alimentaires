# Generated by Django 5.0.4 on 2024-04-21 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0054_ingredientstatus_ingredient_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ingredient",
            name="status",
            field=models.IntegerField(
                choices=[
                    (None, "inconnu"),
                    (1, "autorisé"),
                    (2, "non autorisé"),
                    (3, "à inscrire"),
                    (4, "sans objet"),
                ],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="substance",
            name="status",
            field=models.IntegerField(
                choices=[
                    (None, "inconnu"),
                    (1, "autorisé"),
                    (2, "non autorisé"),
                    (3, "à inscrire"),
                    (4, "sans objet"),
                ],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="plant",
            name="status",
            field=models.IntegerField(
                choices=[
                    (None, "inconnu"),
                    (1, "autorisé"),
                    (2, "non autorisé"),
                    (3, "à inscrire"),
                    (4, "sans objet"),
                ],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
        migrations.AlterField(
            model_name="microorganism",
            name="status",
            field=models.IntegerField(
                choices=[
                    (None, "inconnu"),
                    (1, "autorisé"),
                    (2, "non autorisé"),
                    (3, "à inscrire"),
                    (4, "sans objet"),
                ],
                null=True,
                verbose_name="statut de l'ingrédient ou substance",
            ),
        ),
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
        migrations.DeleteModel(
            name="IngredientStatus",
        ),
    ]
