# Generated by Django 5.1.7 on 2025-03-14 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0125_merge_20250314_1125'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcaIngredient',
            fields=[
                ('ingr_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('vrsdecl_ident', models.IntegerField()),
                ('fctingr_ident', models.IntegerField()),
                ('tying_ident', models.IntegerField()),
                ('ingr_commentaires', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_ingredient',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaIngredientAutre',
            fields=[
                ('ingr_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('inga_ident', models.IntegerField()),
            ],
            options={
                'db_table': 'ica_ingredient_autre',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaMicroOrganisme',
            fields=[
                ('ingr_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('morg_ident', models.IntegerField()),
                ('ingmorg_souche', models.TextField(blank=True, null=True)),
                ('ingmorg_quantite_par_djr', models.BigIntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_micro_organisme',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaPreparation',
            fields=[
                ('ingr_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('plte_ident', models.IntegerField()),
                ('pplan_ident', models.IntegerField(blank=True, null=True)),
                ('unt_ident', models.IntegerField(blank=True, null=True)),
                ('typprep_ident', models.IntegerField(blank=True, null=True)),
                ('prepa_qte', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_preparation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaSubstanceDeclaree',
            fields=[
                ('vrsdecl_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('sbsact_ident', models.IntegerField()),
                ('sbsact_commentaires', models.TextField(blank=True, null=True)),
                ('sbsactdecl_quantite_par_djr', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_substance_declaree',
                'managed': False,
            },
        ),
    ]
