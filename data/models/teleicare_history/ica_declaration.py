# This is an auto-generated Django model module.
# Feel free to rename the models, but don't rename db_table values or field names.
# Pour plus de simplicité, le nom de ces modèles suivent le nom de la table de données provenant du SICCRF,
# initialement stockée dans un système MSSQL,
# et non la nomenclature habituellement utilisée par Compl'Alim

from django.db import models

from .ica_etablissement import IcaEtablissement


class IcaComplementAlimentaire(models.Model):
    cplalim_ident = models.IntegerField(primary_key=True)
    frmgal_ident = models.IntegerField(blank=True, null=True)
    etab = models.ForeignKey(IcaEtablissement, on_delete=models.CASCADE, db_column="etab_ident")
    cplalim_marque = models.TextField(blank=True, null=True)
    cplalim_gamme = models.TextField(blank=True, null=True)
    cplalim_nom = models.TextField()
    dclencours_gout_arome_parfum = models.TextField(blank=True, null=True)
    cplalim_forme_galenique_autre = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_complementalimentaire"


class IcaDeclaration(models.Model):
    # dcl_ident et cplalim_ident sont égaux
    dcl_ident = models.IntegerField(primary_key=True)
    cplalim = models.ForeignKey(IcaComplementAlimentaire, on_delete=models.CASCADE, db_column="cplalim_ident")
    tydcl_ident = models.IntegerField()
    etab = models.ForeignKey(
        IcaEtablissement, on_delete=models.CASCADE, db_column="etab_ident"
    )  # duplique la foreign key vers l'établissement présente dans le CA
    etab_ident_rmm_declarant = models.IntegerField()
    dcl_date = models.TextField()
    dcl_saisie_administration = models.BooleanField()
    dcl_annee = models.IntegerField()
    dcl_mois = models.IntegerField()
    dcl_numero = models.IntegerField()
    dcl_date_fin_commercialisation = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_declaration"


class IcaVersionDeclaration(models.Model):
    vrsdecl_ident = models.IntegerField(primary_key=True)
    ag_ident = models.IntegerField(blank=True, null=True)
    typvrs_ident = models.IntegerField()
    unt_ident = models.IntegerField(blank=True, null=True)
    pays_ident_adre = models.IntegerField(blank=True, null=True)
    etab = models.ForeignKey(
        IcaEtablissement, on_delete=models.CASCADE, db_column="etab_ident"
    )  # duplique la foreign key vers l'établissement présente dans le CA
    ex_ident = models.IntegerField()
    pays_ident_pays_de_reference = models.IntegerField(blank=True, null=True)
    dcl = models.ForeignKey(
        IcaDeclaration, on_delete=models.CASCADE, db_column="dcl_ident"
    )  # dcl_ident est aussi une foreign_key vers IcaComplementAlimentaire
    stattdcl_ident = models.IntegerField(blank=True, null=True)
    stadcl_ident = models.IntegerField(blank=True, null=True)
    vrsdecl_numero = models.IntegerField()
    vrsdecl_commentaires = models.TextField(blank=True, null=True)
    vrsdecl_mise_en_garde = models.TextField(blank=True, null=True)
    vrsdecl_durabilite = models.IntegerField(blank=True, null=True)
    vrsdecl_mode_emploi = models.TextField(blank=True, null=True)
    vrsdecl_djr = models.TextField(blank=True, null=True)
    vrsdecl_conditionnement = models.TextField(blank=True, null=True)
    vrsdecl_poids_uc = models.FloatField(blank=True, null=True)
    vrsdecl_forme_galenique_autre = models.TextField(blank=True, null=True)
    vrsdecl_date_limite_reponse_pro = models.TextField(blank=True, null=True)
    vrsdecl_observations_ac = models.TextField(blank=True, null=True)
    vrsdecl_observations_pro = models.TextField(blank=True, null=True)
    vrsdecl_mode_json = models.BooleanField()
    vrsdecl_numero_dossiel = models.TextField(blank=True, null=True)
    vrsdecl_mode_sans_verif = models.BooleanField()
    vrsdecl_adre_ville = models.TextField(blank=True, null=True)
    vrsdecl_adre_cp = models.TextField(blank=True, null=True)
    vrsdecl_adre_voie = models.TextField(blank=True, null=True)
    vrsdecl_adre_comp = models.TextField(blank=True, null=True)
    vrsdecl_adre_comp2 = models.TextField(blank=True, null=True)
    vrsdecl_adre_dist = models.TextField(blank=True, null=True)
    vrsdecl_adre_region = models.TextField(blank=True, null=True)
    vrsdecl_adre_raison_sociale = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_versiondeclaration"
