# Generated by Django 5.0.7 on 2024-07-31 13:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0078_alter_declaration_conditioning_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="declaredmicroorganism",
            old_name="souche",
            new_name="strain",
        ),
        migrations.RenameField(
            model_name="historicaldeclaredmicroorganism",
            old_name="souche",
            new_name="strain",
        ),
        migrations.AddField(
            model_name="declaredingredient",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR"
            ),
        ),
        migrations.AddField(
            model_name="declaredingredient",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.RESTRICT,
                to="data.substanceunit",
                verbose_name="unité",
            ),
        ),
        migrations.AddField(
            model_name="declaredmicroorganism",
            name="inactivated",
            field=models.BooleanField(
                default=False,
                verbose_name="ayant été inactivé (rendu incapable de réplication)",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredingredient",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR"
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredingredient",
            name="unit",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="data.substanceunit",
                verbose_name="unité",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredmicroorganism",
            name="inactivated",
            field=models.BooleanField(
                default=False,
                verbose_name="ayant été inactivé (rendu incapable de réplication)",
            ),
        ),
        migrations.AlterField(
            model_name="declaredingredient",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="declaredmicroorganism",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="declaredmicroorganism",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR (en UFC)"
            ),
        ),
        migrations.AlterField(
            model_name="declaredplant",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="declaredsubstance",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredingredient",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredmicroorganism",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredmicroorganism",
            name="quantity",
            field=models.FloatField(
                blank=True, null=True, verbose_name="quantité par DJR (en UFC)"
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredplant",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredsubstance",
            name="active",
            field=models.BooleanField(
                default=True,
                verbose_name="ayant une activité physiologique ou nutritionnelle",
            ),
        ),
    ]