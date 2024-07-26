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

/* Tous les emails reliés à une entreprise :
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
    CTACT_NOM,
    CTACT_PRENOM,
    CTACT_TELEPHONE,
    CTACT_FONCTION,
    CTACT_COURRIEL,
    CTACT_TELECOPIE
FROM ICA_ETABLISSEMENT
INNER JOIN ICA_CONTACT ON ICA_ETABLISSEMENT.ETAB_IDENT = ICA_CONTACT.ETAB_IDENT;



/* Les users actifs et leurs emails */
/* La vue V_Users sur aspnet_User filtre les user qui ont effectivement un compte ICA_USAGER ou ICA_ADMINISTRATEUR */
/* Nous créons la vue V_UsersForExport pour extraire les informations nécessaires */
/* TODO: Il faudrait rajouter à cette vue les contact des tables ICA_ETABLISSEMENT et ICA_CONTACT */
CREATE VIEW [dbo].[V_UsersForExport]
AS
   select u.USR_IDENT as UsrIdent,
            u.ADM_IDENT as AdmIdent,
            u.USR_NOM as Nom,
            u.USR_PRENOM as Prenom,
            u.USR_FONCTION as Fonction,
            au.LastActivityDate as LastActivityDate,
            am.Email as Email,
            e.ETAB_RAISON_SOCIALE as EtabRaisonSociale,
            e.ETAB_ENSEIGNE as EtabEnseigne,
            e.Etab_Siret as EtabSiret,
            e.Etab_Numero_Tva_Intra as EtabNumeroTvaIntra,
            e.Etab_Num_Adh_Tele_Proc as EtabNumAdhTeleProc,
            r.RoleName as RoleAsp
from ICA_USAGER as u
                Inner Join Ica_Etablissement as e On u.Etab_Ident = e.Etab_Ident
                Inner Join Aspnet_Users as au On u.UserId = au.UserId
                Inner Join Aspnet_Membership as am On au.UserId = am.UserId and au.ApplicationId = am.ApplicationId
                Inner Join Aspnet_UsersInRoles as uir On uir.UserId = u.UserId
                Inner Join Aspnet_Roles as r on uir.RoleId = r.RoleId
UNION
select null as UsrIdent,
                a.ADM_IDENT as AdmIdent,
                a.ADM_NOM as Nom,
                a.ADM_PRENOM as Prenom,
                a.ADM_FONCTION as Fonction,
                au.LastActivityDate as LastActivityDate,
                am.Email as Email,
                e.ETAB_RAISON_SOCIALE as EtabRaisonSociale,
                e.ETAB_ENSEIGNE as EtabEnseigne,
                e.Etab_Siret as EtabSiret,
                e.Etab_Numero_Tva_Intra as EtabNumeroTvaIntra,
                e.Etab_Num_Adh_Tele_Proc as EtabNumAdhTeleProc,
                r.RoleName as RoleAsp
                from ICA_ADMINISTRATEUR as a
                Inner Join Ica_Etablissement as e On a.Etab_Ident = e.Etab_Ident
                Inner Join Aspnet_Users as au On a.UserId = au.UserId
                Inner Join Aspnet_Membership as am On au.UserId = am.UserId and au.ApplicationId = am.ApplicationId
                Inner Join Aspnet_UsersInRoles as uir On uir.UserId = a.UserId
                Inner Join Aspnet_Roles as r on uir.RoleId = r.RoleId


GO




SELECT COUNT(*) FROM V_UsersForExport
/* 14020 usagers et administrateurs avec Email non null */

/*Extract via PowerShell des utilisateurs ayant eu une activité ces 2 dernières années */
SELECT Nom, Prenom, Email, EtabRaisonSociale, EtabEnseigne, EtabSiret, EtabNumeroTvaIntra, Fonction, RoleAsp FROM [TELEICARE].[dbo].[V_UsersForExport] where LASTACTIVITYDATE > '2022-08-01'


/* Reste à creuser */
/* Toutes les fonctions liées à une entreprise
* soit dans la table ICA_ADMINISTRATEUR
* soit dans la table ICA_CONTACT (table obsolète ?)
* soit dans la table ICA_USAGER
*/


/* Tous les siret liés à une déclaration */
-- creuser dans la table ICA_ETS_CLIENT
