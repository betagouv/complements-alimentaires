/*Compte le nombre d'établissement*/
SELECT COUNT(*) FROM ICA_ETABLISSEMENT;
/* 7209 établissements */

/*Compte le nombre d'administrateur.ice par établissement*/
SELECT
    ETAB_IDENT,
    COUNT(ADM_IDENT) AS NB_ADM
FROM ICA_ADMINISTRATEUR
GROUP BY ETAB_IDENT
HAVING COUNT(ADM_IDENT) != 1;
/* 1 seul administrateur.ice par établissement*/
/* 6558 administrateur.ice => il y a des établissements sans administrateur.ice */

/* Compte le nombre de contact par établissement*/
SELECT
    NB_CTACT,
    COUNT(ETAB_IDENT) AS NB_ETAB
FROM (
    SELECT
        ETAB_IDENT,
        COUNT(CTACT_IDENT) AS NB_CTACT
    FROM ICA_CONTACT
    GROUP BY ETAB_IDENT
) AS SUB_TABLE GROUP BY NB_CTACT;
-- NB_CTACT NB_ETAB
-- 1    229
-- 2    26
-- 3    7
-- 4    1
/* Il y a beaucoup d'établissements sans contact */
SELECT COUNT(*)
FROM ICA_ETABLISSEMENT
LEFT OUTER JOIN
    ICA_CONTACT
    ON ICA_ETABLISSEMENT.ETAB_IDENT = ICA_CONTACT.ETAB_IDENT
WHERE ICA_CONTACT.ETAB_IDENT IS NULL
/* 6946 établissements sans contact, et 306 contacts seulement */
/* Hypothèse : ICA_CONTACT était obsolète */

/* Compte le nombre d'usager par établissement*/
SELECT
    NB_USER,
    COUNT(ETAB_IDENT) AS NB_ETAB
FROM (
    SELECT
        ADM_IDENT,
        ETAB_IDENT,
        COUNT(USR_IDENT) AS NB_USER
    FROM ICA_USAGER GROUP BY ADM_IDENT, ETAB_IDENT
) AS SUB_TABLE GROUP BY NB_USER ORDER BY NB_USER DESC;
-- NB_USER  NB_ETAB
-- 12   1
-- 11   1
-- 10   4
-- 9    4
-- 8    2
-- 7    8
-- 6    18
-- 5    26
-- 4    58
-- 3    91
-- 2    296
-- 1    6778




/* Calcul des contact qui sont aussi administrateur.ice = même nom, adresse mail, téléphone */

/* Tous les courriels reliés à une entreprise :
* soit dans la table ICA_ETABLISSEMENT
* soit dans la table ICA_CONTACT
 */
SELECT
    ETAB_SIRET,
    ETAB_NUMERO_TVA_INTRA,
    ETAB_RAISON_SOCIALE,
    ETAB_ENSEIGNE,
    ETAB_TELEPHONE,
    ETAB_COURRIEL,
    ETAB_SITE_INTERNET,
    ETAB_NUM_ADH_TELE_PROC,
    ETAB_DATE_ADHESION,
    ADM_NOM,
    ADM_PRENOM,
    ADM_FONCTION,
    ADM_TELECOPIE,
    ADM_TELEPHONE,
    CTACT_NOM,
    CTACT_PRENOM,
    CTACT_TELEPHONE,
    CTACT_FONCTION,
    CTACT_COURRIEL,
    CTACT_TELECOPIE
FROM ICA_ETABLISSEMENT
INNER JOIN
    ICA_ADMINISTRATEUR
    ON ICA_ETABLISSEMENT.ETAB_IDENT = ICA_ADMINISTRATEUR.ETAB_IDENT
INNER JOIN ICA_CONTACT ON ICA_ETABLISSEMENT.ETAB_IDENT = ICA_CONTACT.ETAB_IDENT;

/* Toutes les fonctions liées à une entreprise
* soit dans la table ICA_ADMINISTRATEUR
* soit dans la table ICA_CONTACT
* soit dans la table ICA_USAGER
*/


/* Tous les siret liés à une déclaration */
--   join ICA_ETS_CLIENT
-- [ETAB_CLIENT_SIRET]

/* Les users actifs */
-- [aspnet_Users] [LastActivityDate]


-- [Aspnet_Membership_2021_09_13] [Email]
