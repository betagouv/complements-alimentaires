# Generated by Django 5.1 on 2024-08-13 09:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0084_rename_cosupervisionclaim_companyaccessclaim_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="companyaccessclaim",
            name="declarant_role",
            field=models.BooleanField(
                default=False, verbose_name="demande de rôle déclarant"
            ),
        ),
        migrations.AddField(
            model_name="companyaccessclaim",
            name="supervisor_role",
            field=models.BooleanField(
                default=False, verbose_name="demande de rôle gestionnaire"
            ),
        ),
    ]