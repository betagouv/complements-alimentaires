# This is an auto-generated Django model module.
# Feel free to rename the models, but don't rename db_table values or field names.
# Pour plus de simplicité, le nom de ces modèles suivent le nom de la table de données provenant du SICCRF,
# initialement stockée dans un système MSSQL,
# et non la nomenclature habituellement utilisée par Compl'Alim

from django.db import models


class IcaIngredient(models.Model):
    ingr_ident = models.IntegerField(primary_key=True)
    vrsdecl_ident = models.IntegerField()
    fctingr_ident = models.IntegerField()
    tying_ident = models.IntegerField()
    ingr_commentaires = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_ingredient"


class IcaIngredientAutre(models.Model):
    ingr_ident = models.IntegerField(primary_key=True)
    inga_ident = models.IntegerField()

    class Meta:
        managed = False
        db_table = "ica_ingredient_autre"


class IcaMicroOrganisme(models.Model):
    ingr_ident = models.IntegerField(primary_key=True)
    morg_ident = models.IntegerField()
    ingmorg_souche = models.TextField(blank=True, null=True)
    ingmorg_quantite_par_djr = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_micro_organisme"


class IcaPreparation(models.Model):
    ingr_ident = models.IntegerField(primary_key=True)
    plte_ident = models.IntegerField()
    pplan_ident = models.IntegerField(blank=True, null=True)
    unt_ident = models.IntegerField(blank=True, null=True)
    typprep_ident = models.IntegerField(blank=True, null=True)
    prepa_qte = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_preparation"


class IcaSubstanceDeclaree(models.Model):
    vrsdecl_ident = models.IntegerField(
        primary_key=True
    )  # The composite primary key (vrsdecl_ident, sbsact_ident) found, that is not supported. The first column is selected.
    sbsact_ident = models.IntegerField()
    sbsact_commentaires = models.TextField(blank=True, null=True)
    sbsactdecl_quantite_par_djr = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "ica_substance_declaree"
        unique_together = (("vrsdecl_ident", "sbsact_ident"),)
