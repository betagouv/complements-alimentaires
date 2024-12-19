# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class IcaEtablissement(models.Model):
    etab_ident = models.IntegerField(primary_key=True)
    cog_ident = models.IntegerField(blank=True, null=True)
    etab_ident_parent = models.IntegerField(blank=True, null=True)
    pays_ident = models.IntegerField()
    etab_siret = models.TextField(blank=True, null=True)
    etab_numero_tva_integerra = models.TextField(blank=True, null=True)
    etab_raison_sociale = models.TextField()
    etab_enseigne = models.TextField(blank=True, null=True)
    etab_adre_ville = models.TextField(blank=True, null=True)
    etab_adre_cp = models.TextField(blank=True, null=True)
    etab_adre_voie = models.TextField(blank=True, null=True)
    etab_adre_comp = models.TextField(blank=True, null=True)
    etab_adre_comp2 = models.TextField(blank=True, null=True)
    etab_adre_dist = models.TextField(blank=True, null=True)
    etab_telephone = models.TextField(blank=True, null=True)
    etab_fax = models.TextField(blank=True, null=True)
    etab_courriel = models.TextField(blank=True, null=True)
    etab_site_internet = models.TextField(blank=True, null=True)
    etab_ica_faconnier = models.BooleanField(blank=True, null=True)
    etab_ica_fabricant = models.BooleanField(blank=True, null=True)
    etab_ica_conseil = models.BooleanField(blank=True, null=True)
    etab_ica_importateur = models.BooleanField(blank=True, null=True)
    etab_ica_introducteur = models.BooleanField(blank=True, null=True)
    etab_ica_distributeur = models.BooleanField(blank=True, null=True)
    etab_ica_enseigne = models.TextField(blank=True, null=True)
    etab_adre_region = models.TextField(blank=True, null=True)
    etab_dt_ajout_ident_parent = models.TextField(blank=True, null=True)
    etab_num_adh_tele_proc = models.TextField(blank=True, null=True)
    etab_commentaire_ident_parent = models.TextField(blank=True, null=True)
    etab_nom_domaine = models.TextField(blank=True, null=True)
    etab_date_adhesion = models.TextField(blank=True, null=True)
    etab_nb_compte_autorise = models.IntegerField()

    class Meta:
        managed = False
        db_table = "ica_etablissement"
