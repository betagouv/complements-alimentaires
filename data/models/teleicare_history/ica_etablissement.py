# This is an auto-generated Django model module.
# Feel free to rename the models, but don't rename db_table values or field names.
# Pour plus de simplicité, le nom de ce modèle suit le nom de la table de données provenant du SICCRF,
# initialement stockée dans un système MSSQL,
# et non la nomenclature habituellement utilisée par Compl'Alim
from django.db import models


class IcaEtablissement(models.Model):
    etab_ident = models.IntegerField(primary_key=True)
    cog_ident = models.IntegerField(blank=True, null=True)
    etab_ident_parent = models.IntegerField(blank=True, null=True)
    pays_ident = models.IntegerField()
    etab_siret = models.CharField(blank=True, null=True)
    etab_numero_tva_intra = models.CharField(blank=True, null=True)
    etab_raison_sociale = models.TextField()
    etab_enseigne = models.TextField(blank=True, null=True)
    etab_adre_ville = models.CharField(blank=True, null=True)
    etab_adre_cp = models.CharField(blank=True, null=True)
    etab_adre_voie = models.CharField(blank=True, null=True)
    etab_adre_comp = models.CharField(blank=True, null=True)
    etab_adre_comp2 = models.CharField(blank=True, null=True)
    etab_adre_dist = models.CharField(blank=True, null=True)
    etab_telephone = models.CharField(blank=True, null=True)
    etab_fax = models.CharField(blank=True, null=True)
    etab_courriel = models.CharField(blank=True, null=True)
    etab_site_internet = models.CharField(blank=True, null=True)
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

    def __str__(self):
        return f"{self.etab_raison_sociale}"
