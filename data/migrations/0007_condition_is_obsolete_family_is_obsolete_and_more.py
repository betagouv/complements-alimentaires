# Generated by Django 4.2.7 on 2023-12-12 08:59

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data", "0006_rename_substance_ingredient_substances_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="condition",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="family",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="ingredientsynonym",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="microorganismsynonym",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="plantpart",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="plantsynonym",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="population",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AddField(
            model_name="substancesynonym",
            name="is_obsolete",
            field=models.BooleanField(
                default=False, verbose_name="ingrédient obsolète"
            ),
        ),
        migrations.AlterField(
            model_name="condition",
            name="name",
            field=models.TextField(verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="plantsynonym",
            name="name",
            field=models.TextField(verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="population",
            name="name",
            field=models.TextField(verbose_name="nom"),
        ),
        migrations.AlterField(
            model_name="substancesynonym",
            name="name",
            field=models.TextField(verbose_name="nom"),
        ),
    ]
