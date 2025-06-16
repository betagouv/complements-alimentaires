# Changelog

Tous les changements notables apportés aux jeux de données exposés sur data.gouv.fr vont être documentés ici.

## 2025-01-23 - Modification
 - Remplacer dans la colonne `Facteurs Risques` les valeurs 'Autres (à préciser)' par les valeurs renseignées par l'utilisateur
 - Remplacer dans la colonne `Objectif Effets` les valeurs 'Autres (à préciser)' par les valeurs renseignées par l'utilisateur

## 2025-01-16 - Ajout
- Champ Date décision
- Champ Article de référence
- Champ Objectifs effets
- Champ Aromes
- Champ Facteurs riques
- Champ Populations cibles
- Champ ingrédients inactifs
- Champ Additifs
- Champ Nutriments
- Champ Autres Ingrédients Actifs

## 2025-01-17 - Augmentation des données
- 56160 déclarations historiques importées de TeleIcare avec leurs champs :
  -id
  -decision
  -nom_commercial
  -marque
  -gamme
  -responsable_mise_sur_marche
  -siret_responsable_mise_sur_marche
  -forme_galenique
  -dose_journaliere
  -mode_emploi
  -mises_en_garde


## 2025-02-04 - Augmentation des données
- ajout des champs de compositions des 56160 déclarations historiques importées de TeleIcare :
  -plantes
  -micro_organismes
  -substances

## 2025-04-07 - Amélioration qualité données
- le champ id contient l'identifiant TeleIcare ou Compl'Alim
- les champs complexes ['objectif_effet', 'facteurs_risques', 'populations_cibles', 'additifs', 'nutriments', 'autres_ingredients_actifs', 'ingredients_inactifs'] sont écrit comme des JSON string conformes

## 2025-04-30 - Amélioration qualité données
- le champ id contient l'identifiant TeleIcare ou Compl'Alim
- le champ numero_declaration_teleicare contient le numéro de déclaration si la déclaration a été faite dans la plateforme historique TeleIcare

## 2025-05-19 - Ajout
- champ vat_responsable_mise_sur_marche
- entièreté de l'historique de déclarations déclarées dans TeleIcare

## 2025-06-23 - Ajout
- le champ id contient uniquement l'identifiant Compl'Alim
- le champ teleicare_id contient uniquement l'identifiant Teleicare (si concerné)
