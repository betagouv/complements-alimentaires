# Generated by Django 5.1 on 2024-09-05 09:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0090_alter_declaration_article_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="declaredingredient",
            options={
                "verbose_name": "ingredient déclaré",
                "verbose_name_plural": "ingredients déclarés",
            },
        ),
        migrations.AlterModelOptions(
            name="declaredmicroorganism",
            options={
                "verbose_name": "microorganisme déclaré",
                "verbose_name_plural": "microorganismes déclarés",
            },
        ),
        migrations.AlterModelOptions(
            name="declaredplant",
            options={
                "verbose_name": "plante déclarée",
                "verbose_name_plural": "plantes déclarées",
            },
        ),
        migrations.AlterModelOptions(
            name="declaredsubstance",
            options={
                "verbose_name": "substance déclarée",
                "verbose_name_plural": "substances déclarées",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldeclaredingredient",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical ingredient déclaré",
                "verbose_name_plural": "historical ingredients déclarés",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldeclaredmicroorganism",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical microorganisme déclaré",
                "verbose_name_plural": "historical microorganismes déclarés",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldeclaredplant",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical plante déclarée",
                "verbose_name_plural": "historical plantes déclarées",
            },
        ),
        migrations.AlterModelOptions(
            name="historicaldeclaredsubstance",
            options={
                "get_latest_by": ("history_date", "history_id"),
                "ordering": ("-history_date", "-history_id"),
                "verbose_name": "historical substance déclarée",
                "verbose_name_plural": "historical substances déclarées",
            },
        ),
        migrations.AddField(
            model_name="declaredingredient",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
        migrations.AddField(
            model_name="declaredmicroorganism",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
        migrations.AddField(
            model_name="declaredplant",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredingredient",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredmicroorganism",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
        migrations.AddField(
            model_name="historicaldeclaredplant",
            name="first_ocurrence",
            field=models.BooleanField(
                default=False,
                verbose_name="Est-ce que cet ingrédient a été rajouté en base suite à cette déclaration ?",
            ),
        ),
    ]
