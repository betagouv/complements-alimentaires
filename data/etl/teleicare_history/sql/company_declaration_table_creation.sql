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


CREATE TABLE ICA_COMPLEMENTALIMENTAIRE (
    CPLALIM_IDENT integer PRIMARY KEY,
    FRMGAL_IDENT integer NULL,
    -- toujours le même que celui indiqué dans ICA_VERSIONDECLARATION
    ETAB_IDENT integer NOT NULL,
    CPLALIM_MARQUE text NULL,
    CPLALIM_GAMME text NULL,
    CPLALIM_NOM text NOT NULL,
    DCLENCOURS_GOUT_AROME_PARFUM text NULL,
    CPLALIM_FORME_GALENIQUE_AUTRE text NULL
);


CREATE TABLE ICA_DECLARATION (
    DCL_IDENT integer PRIMARY KEY,
    CPLALIM_IDENT integer NOT NULL, -- dcl_ident et cplalim_ident sont égaux
    TYDCL_IDENT integer NOT NULL,
    ETAB_IDENT integer NULL, -- si différent de NULL c'est parce qu'il est différent de celui dans ICA_COMPLEMENTALIMENTAIRE et ICA_VERSIONDECLARATION, c'est l'id de l'entp mandatée (qui déclare pour une autre)
    ETAB_IDENT_RMM_DECLARANT integer NOT NULL,
    DCL_DATE text NOT NULL,
    DCL_SAISIE_ADMINISTRATION boolean NOT NULL,
    DCL_ANNEE integer NOT NULL,
    DCL_MOIS integer NOT NULL,
    DCL_NUMERO integer NOT NULL,
    DCL_DATE_FIN_COMMERCIALISATION text NULL
);


CREATE TABLE ICA_VERSIONDECLARATION (
    VRSDECL_IDENT integer PRIMARY KEY,
    AG_IDENT integer NULL,
    TYPVRS_IDENT integer NOT NULL, -- le type de version de déclaration
    UNT_IDENT integer NULL,
    PAYS_IDENT_ADRE integer NULL,
    -- toujours le même que celui indiqué dans ICA_COMPLEMENTALIMENTAIRE
    ETAB_IDENT integer NULL,
    EX_IDENT integer NOT NULL, -- le stade d'examen de la déclaration
    PAYS_IDENT_PAYS_DE_REFERENCE integer NULL,
    DCL_IDENT integer NOT NULL,
    STATTDCL_IDENT integer NULL, -- le status de la déclaration
    STADCL_IDENT integer NULL, -- le stade de la déclaration
    VRSDECL_NUMERO integer NOT NULL, -- veut dire quoi ?
    VRSDECL_COMMENTAIRES text NULL,
    VRSDECL_MISE_EN_GARDE text NULL,
    VRSDECL_DURABILITE integer NULL,
    VRSDECL_MODE_EMPLOI text NULL,
    VRSDECL_DJR text NULL,
    VRSDECL_CONDITIONNEMENT text NULL,
    VRSDECL_POIDS_UC float NULL,
    VRSDECL_FORME_GALENIQUE_AUTRE text NULL,
    VRSDECL_DATE_LIMITE_REPONSE_PRO text NULL,
    VRSDECL_OBSERVATIONS_AC text NULL,
    VRSDECL_OBSERVATIONS_PRO text NULL,
    VRSDECL_MODE_JSON boolean NOT NULL,
    VRSDECL_NUMERO_DOSSIEL text NULL,
    VRSDECL_MODE_SANS_VERIF boolean NOT NULL,
    VRSDECL_ADRE_VILLE text NULL,
    VRSDECL_ADRE_CP text NULL,
    VRSDECL_ADRE_VOIE text NULL,
    VRSDECL_ADRE_COMP text NULL,
    VRSDECL_ADRE_COMP2 text NULL,
    VRSDECL_ADRE_DIST text NULL,
    VRSDECL_ADRE_REGION text NULL,
    VRSDECL_ADRE_RAISON_SOCIALE text NULL
);


-- EX_IDENT
-- when 1 then 'en attente'
-- when 2 then 'examen'
-- when 3 then 'validation'
-- when 4 then 'signature'
-- when 5 then 'envoi'
-- when 6 then 'reexamen'
-- when 7 then 'terminé'

-- STATTDCL_IDENT
-- when 1 then 'en cours'
-- when 2 then 'autorisé temporaire'
-- when 3 then 'autorisé prolongé'
-- when 4 then 'autorisé définitif'
-- when 5 then 'refusé'
-- when 6 then 'arrêt commercialisation'
-- when 7 then 'retiré du marché'
-- when 8 then 'abandonné'

-- STADCL_IDENT
-- when 1 then 'saisie par administration'
-- when 2 then 'en préparation'
-- when 3 then 'en cours'
-- when 4 then 'en attente compléments'
-- when 5 then 'en attente observations'
-- when 6 then 'compléments hors délais'
-- when 7 then 'non autorisé (HD)'
-- when 8 then 'clos'


-- TYPVRS_IDENT
-- when 1 then 'nouvelle'
-- when 2 then 'compléments d'information'
-- when 3 then 'observation'



CREATE TABLE ICA_POPULATION_CIBLE_DECLAREE (
    VRSDECL_IDENT integer NOT NULL,
    POPCBL_IDENT integer NOT NULL,
    VRSPCB_POPCIBLE_AUTRE text NULL,
    PRIMARY KEY (VRSDECL_IDENT, POPCBL_IDENT)
);




CREATE TABLE ICA_POPULATION_RISQUE_DECLAREE (
    VRSDECL_IDENT integer NOT NULL,
    POPRS_IDENT integer NOT NULL,
    VRSPRS_POPRISQUE_AUTRE text NULL,
    PRIMARY KEY (VRSDECL_IDENT, POPRS_IDENT)
);
