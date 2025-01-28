-- Le but de ce fichier est de permettre la recréation des tables Teleicare correspondant
-- au modèle de Declaration Compl'Alim


-- int int smallint -> integer
-- vachar -> text
-- bit -> boolean
-- datetime -> text (pour une conversion ensuite)

CREATE TABLE ICA_ETABLISSEMENT (
    ETAB_IDENT integer PRIMARY KEY,
    COG_IDENT integer NULL,
    ETAB_IDENT_PARENT integer NULL,
    PAYS_IDENT integer NOT NULL,
    ETAB_SIRET text NULL,
    ETAB_NUMERO_TVA_INTRA text NULL,
    ETAB_RAISON_SOCIALE text NOT NULL,
    ETAB_ENSEIGNE text NULL,
    ETAB_ADRE_VILLE text NULL,
    ETAB_ADRE_CP text NULL,
    ETAB_ADRE_VOIE text NULL,
    ETAB_ADRE_COMP text NULL,
    ETAB_ADRE_COMP2 text NULL,
    ETAB_ADRE_DIST text NULL,
    ETAB_TELEPHONE text NULL,
    ETAB_FAX text NULL,
    ETAB_COURRIEL text NULL,
    ETAB_SITE_INTERNET text NULL,
    ETAB_ICA_FACONNIER boolean NULL,
    ETAB_ICA_FABRICANT boolean NULL,
    ETAB_ICA_CONSEIL boolean NULL,
    ETAB_ICA_IMPORTATEUR boolean NULL,
    ETAB_ICA_INTRODUCTEUR boolean NULL,
    ETAB_ICA_DISTRIBUTEUR boolean NULL,
    ETAB_ICA_ENSEIGNE text NULL,
    ETAB_ADRE_REGION text NULL,
    ETAB_DT_AJOUT_IDENT_PARENT text NULL,
    ETAB_NUM_ADH_TELE_PROC text NULL,
    ETAB_COMMENTAIRE_IDENT_PARENT text NULL,
    ETAB_NOM_DOMAINE text NULL,
    ETAB_DATE_ADHESION text NULL,
    ETAB_NB_COMPTE_AUTORISE integer NOT NULL
);
