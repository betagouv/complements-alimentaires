# Generated by Django 5.1.7 on 2025-05-30 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0150_alter_historicalingredient_to_be_entered_in_next_decree_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalingredient',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='historicalingredient',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='historicalmicroorganism',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='historicalmicroorganism',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='historicalplant',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='historicalplant',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='historicalsubstance',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='historicalsubstance',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='ingredient',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='microorganism',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='microorganism',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='plant',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
        migrations.AlterField(
            model_name='substance',
            name='ca_private_comments',
            field=models.TextField(blank=True, verbose_name='commentaires privés CA'),
        ),
        migrations.AlterField(
            model_name='substance',
            name='ca_public_comments',
            field=models.TextField(blank=True, verbose_name='commentaires publics CA'),
        ),
    ]
