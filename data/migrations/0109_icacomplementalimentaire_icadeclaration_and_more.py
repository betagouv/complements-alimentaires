# Generated by Django 5.1.4 on 2024-12-20 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0108_merge_20241205_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='IcaComplementAlimentaire',
            fields=[
                ('cplalim_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('frmgal_ident', models.IntegerField(blank=True, null=True)),
                ('cplalim_marque', models.TextField(blank=True, null=True)),
                ('cplalim_gamme', models.TextField(blank=True, null=True)),
                ('cplalim_nom', models.TextField()),
                ('dclencours_gout_arome_parfum', models.TextField(blank=True, null=True)),
                ('cplalim_forme_galenique_autre', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_complementalimentaire',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaDeclaration',
            fields=[
                ('dcl_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('tydcl_ident', models.IntegerField()),
                ('etab_ident_rmm_declarant', models.IntegerField()),
                ('dcl_date', models.TextField()),
                ('dcl_saisie_administration', models.BooleanField()),
                ('dcl_annee', models.IntegerField()),
                ('dcl_mois', models.IntegerField()),
                ('dcl_numero', models.IntegerField()),
                ('dcl_date_fin_commercialisation', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_declaration',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaEtablissement',
            fields=[
                ('etab_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('cog_ident', models.IntegerField(blank=True, null=True)),
                ('etab_ident_parent', models.IntegerField(blank=True, null=True)),
                ('pays_ident', models.IntegerField()),
                ('etab_siret', models.TextField(blank=True, null=True)),
                ('etab_numero_tva_intra', models.TextField(blank=True, null=True)),
                ('etab_raison_sociale', models.TextField()),
                ('etab_enseigne', models.TextField(blank=True, null=True)),
                ('etab_adre_ville', models.TextField(blank=True, null=True)),
                ('etab_adre_cp', models.TextField(blank=True, null=True)),
                ('etab_adre_voie', models.TextField(blank=True, null=True)),
                ('etab_adre_comp', models.TextField(blank=True, null=True)),
                ('etab_adre_comp2', models.TextField(blank=True, null=True)),
                ('etab_adre_dist', models.TextField(blank=True, null=True)),
                ('etab_telephone', models.TextField(blank=True, null=True)),
                ('etab_fax', models.TextField(blank=True, null=True)),
                ('etab_courriel', models.TextField(blank=True, null=True)),
                ('etab_site_internet', models.TextField(blank=True, null=True)),
                ('etab_ica_faconnier', models.BooleanField(blank=True, null=True)),
                ('etab_ica_fabricant', models.BooleanField(blank=True, null=True)),
                ('etab_ica_conseil', models.BooleanField(blank=True, null=True)),
                ('etab_ica_importateur', models.BooleanField(blank=True, null=True)),
                ('etab_ica_introducteur', models.BooleanField(blank=True, null=True)),
                ('etab_ica_distributeur', models.BooleanField(blank=True, null=True)),
                ('etab_ica_enseigne', models.TextField(blank=True, null=True)),
                ('etab_adre_region', models.TextField(blank=True, null=True)),
                ('etab_dt_ajout_ident_parent', models.TextField(blank=True, null=True)),
                ('etab_num_adh_tele_proc', models.TextField(blank=True, null=True)),
                ('etab_commentaire_ident_parent', models.TextField(blank=True, null=True)),
                ('etab_nom_domaine', models.TextField(blank=True, null=True)),
                ('etab_date_adhesion', models.TextField(blank=True, null=True)),
                ('etab_nb_compte_autorise', models.IntegerField()),
            ],
            options={
                'db_table': 'ica_etablissement',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='IcaVersionDeclaration',
            fields=[
                ('vrsdecl_ident', models.IntegerField(primary_key=True, serialize=False)),
                ('ag_ident', models.IntegerField(blank=True, null=True)),
                ('typvrs_ident', models.IntegerField()),
                ('unt_ident', models.IntegerField(blank=True, null=True)),
                ('pays_ident_adre', models.IntegerField(blank=True, null=True)),
                ('ex_ident', models.IntegerField()),
                ('pays_ident_pays_de_reference', models.IntegerField(blank=True, null=True)),
                ('stattdcl_ident', models.IntegerField(blank=True, null=True)),
                ('stadcl_ident', models.IntegerField(blank=True, null=True)),
                ('vrsdecl_numero', models.IntegerField()),
                ('vrsdecl_commentaires', models.TextField(blank=True, null=True)),
                ('vrsdecl_mise_en_garde', models.TextField(blank=True, null=True)),
                ('vrsdecl_durabilite', models.IntegerField(blank=True, null=True)),
                ('vrsdecl_mode_emploi', models.TextField(blank=True, null=True)),
                ('vrsdecl_djr', models.TextField(blank=True, null=True)),
                ('vrsdecl_conditionnement', models.TextField(blank=True, null=True)),
                ('vrsdecl_poids_uc', models.FloatField(blank=True, null=True)),
                ('vrsdecl_forme_galenique_autre', models.TextField(blank=True, null=True)),
                ('vrsdecl_date_limite_reponse_pro', models.TextField(blank=True, null=True)),
                ('vrsdecl_observations_ac', models.TextField(blank=True, null=True)),
                ('vrsdecl_observations_pro', models.TextField(blank=True, null=True)),
                ('vrsdecl_mode_json', models.BooleanField()),
                ('vrsdecl_numero_dossiel', models.TextField(blank=True, null=True)),
                ('vrsdecl_mode_sans_verif', models.BooleanField()),
                ('vrsdecl_adre_ville', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_cp', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_voie', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_comp', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_comp2', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_dist', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_region', models.TextField(blank=True, null=True)),
                ('vrsdecl_adre_raison_sociale', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'ica_versiondeclaration',
                'managed': False,
            },
        ),
        migrations.AddField(
            model_name='company',
            name='siccrf_id',
            field=models.IntegerField(blank=True, db_index=True, editable=False, null=True, unique=True, verbose_name='id dans les tables et tables relationnelles SICCRF'),
        ),
    ]