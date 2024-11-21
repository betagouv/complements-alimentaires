# Generated by Django 5.1.3 on 2024-11-19 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0103_merge_20241118_1426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalingredient',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='historicalmicroorganism',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='historicalplant',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='historicalsubstance',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='microorganism',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
        migrations.AlterField(
            model_name='substance',
            name='novel_food',
            field=models.BooleanField(default=False, verbose_name='considéré Novel Food ?'),
        ),
    ]
