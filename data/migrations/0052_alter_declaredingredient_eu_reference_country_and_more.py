# Generated by Django 5.0.3 on 2024-04-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data", "0051_remove_declaration_galenic_formulation_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="declaredingredient",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
        migrations.AlterField(
            model_name="declaredmicroorganism",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
        migrations.AlterField(
            model_name="declaredplant",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredingredient",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredmicroorganism",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
        migrations.AlterField(
            model_name="historicaldeclaredplant",
            name="eu_reference_country",
            field=models.CharField(
                blank=True,
                choices=[
                    ("FR", "France"),
                    ("DE", "Allemagne"),
                    ("AT", "Autriche"),
                    ("BE", "Belgique"),
                    ("BG", "Bulgarie"),
                    ("CY", "Chypre"),
                    ("HR", "Croatie"),
                    ("DK", "Danemark"),
                    ("ES", "Espagne"),
                    ("EE", "Estonie"),
                    ("FI", "Finlande"),
                    ("GR", "Grèce"),
                    ("HU", "Hongrie"),
                    ("IE", "Irlande"),
                    ("NI", "Irlande du Nord"),
                    ("IS", "Islande"),
                    ("IT", "Italie"),
                    ("LV", "Lettonie"),
                    ("LI", "Liechtenstein"),
                    ("LT", "Lituanie"),
                    ("LU", "Luxembourg"),
                    ("MT", "Malte"),
                    ("NO", "Norvège"),
                    ("NL", "Pays-Bas"),
                    ("PL", "Pologne"),
                    ("PT", "Portugal"),
                    ("RO", "Roumanie"),
                    ("SK", "Slovaquie"),
                    ("SI", "Slovénie"),
                    ("SE", "Suède"),
                    ("CZ", "République Tchèque"),
                ],
                default="FR",
                verbose_name="pays de source réglementaire",
            ),
        ),
    ]
