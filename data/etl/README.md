# Général

L'ETL permet d'extraire des données issues de la plateforme vers data.gouv.fr pour l'ouverture en open-data.
Pour administrer ce(s) jeu(x) de données, il faut demander (au directeur de projet "Données" SNUM/SDSPR/....) un accès à l'organisation du MASA pour publier/administrer des jeux de données.

Les jeux de données édités et publiés :

    * déclarations de compléments alimentaires autorisés

## Open Data

Les données sont stockées sur notre S3 puis référencées depuis l'intertace d'administration de data.gouv.fr (compte perso, affiliation nécessaire à l'organisme MASA).

L'API de data.gouv.fr est utilisée afin de "notifier" data.gouv.fr des mises à jour de fichier et ainsi permettre d'afficher les informations correctes sur la fréquence de mise à jour ainsi que la date de la dernière modification.

Nous validons les jeux de données en couplant l'outil validata avec le schéma de donnée de chaque jeu.
