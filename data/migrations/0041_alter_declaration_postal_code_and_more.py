# Generated by Django 5.0.3 on 2024-04-03 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0040_alter_declaration_unit_measurement_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaration",
            name="postal_code",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="code postal"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaration",
            name="postal_code",
            field=models.CharField(
                blank=True, max_length=10, verbose_name="code postal"
            ),
        ),
    ]
