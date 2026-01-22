# Compléments Alimentaires

## Installation du projet

Il existe 2 méthodes distinctes d'installation pour ce projet :
1) l'installation manuelle classique
2) l'installation avec Docker


### Installation manuelle classique (_méthode 1_)


#### À installer localement

- [Python3](https://www.python.org/downloads/) (version 3.11)
- [pip](https://pip.pypa.io/en/stable/installing/) (souvent installé avec Python)
- [Node et npm](https://nodejs.org/en/download/) (version 20 LTS)
- [Postgres](https://www.postgresql.org/download/) (version 15)

#### Création d'un environnement Python3

Pour commencer, c'est recommandé de créer un environnement virtuel avec Python3.

```
python -m venv venv
source ./venv/bin/activate
```

#### Installer les dépendances du backend

Les dépendances du backend se trouvent dans `requirements.txt`. Pour les installer :

```
pip install -r requirements.txt
```

#### Installer les dépendances du frontend

L'application frontend se trouve sous `/frontend`. Pour installer les dépendances :

```
cd frontend
npm ci
```

#### Créer la base de données

Par exemple, pour utiliser une base de données nommée _complalim_db_ :

```
createdb complalim_db
```
Le user doit avoir les droits de creation

```
sudo su postgres
postgres=# create user <DB_USER> createdb password <DB_PASSWORD>;
```

#### Pre-commit

On utilise l'outil [`pre-commit`](https://pre-commit.com/) pour effectuer des vérifications automatiques
avant chaque commit. Cela permet par exemple de linter les code Python, Javascript et HTML.

Pour pouvoir l'utiliser, assurez-vous d'être dans votre environnement virtuel, et activez-le avec `pre-commit install`.

Les vérifications seront ensuite effectuées avant chaque commit. Attention, lorsqu'une vérification `fail`,
le commit est annulé. Il faut donc que toutes les vérifications passent pour que le commit soit pris en
compte. Si exceptionnellement vous voulez commiter malgré qu'une vérification ne passe pas, c'est possible
avec `git commit -m 'my message' --no-verify`.

### Installation avec docker (_méthode 2_)

Créez un fichier `.env`. Copiez les variables d'environnement `DB_NAME`, `DB_PORT`, `DB_PASSWORD` dedans. C'est nécessaire car `compose.yaml` [ne permets pas](https://github.com/docker/compose/issues/11755) l'interpolation avec les variables définit dans un fichier indiqué par `env_file`, que `.env`.

```
make build
make run
make bash
python manage.py migrate
```

[Suivre les instructions](#import-de-données-initiales-fixtures) pour initialiser la BDD et créer un super user.

## Configuration du projet

_À suivre peu importe la méthode d'installation choisie_

#### Compléter les variables d'environnement

L'application utilise [django-environ](https://django-environ.readthedocs.io/en/latest/), vous pouvez donc créer un fichier `.env` à la racine du projet avec ces variables définies :

```
SECRET= Le secret pour Django (vous pouvez le [générer ici](https://djecrety.ir/))
DEBUG= `True` pour le développement local ou `False` autrement
DB_USER= L'utilisateur de la base de données. Doit avoir les droits de creation de db pour les tests.
DB_PASSWORD= Le mot de passe pour accéder à la base de données
DB_HOST= Le host de la base de données (par ex. '127.0.0.1')
DB_PORT= Le port de la base de données (par ex. '3306')
DB_NAME= Le nom de la base de données (par ex. 'complements-alimentaires'
HOSTNAME= Le hostname dans lequel l'application se trouve (par ex. 127.0.0.1:8000)
ALLOWED_HOSTS= Des noms de domaine/d’hôte que ce site peut servir (par ex. 'localhost, \*')
EMAIL_BACKEND= par ex. 'django.core.mail.backends.console.EmailBackend'. Pour utiliser SendInBlue : 'anymail.backends.sendinblue.EmailBackend'
DEFAULT_FROM_EMAIL= par ex. 'from@example.com'
CONTACT_EMAIL= par ex. 'contact@example.com'
STATICFILES_STORAGE= Le système utilisé pour les fichiers statiques (par ex. 'django.contrib.staticfiles.storage.StaticFilesStorage')
DEFAULT_FILE_STORAGE= Le système de stockage de fichiers (par ex 'django.core.files.storage.FileSystemStorage')
FORCE_HTTPS= 'False' si on développe en local, 'True' autrement
SECURE= 'False' si on développe en local, 'True' autrement
ENVIRONMENT= Optionnel - si cette variable est remplie un badge sera visible dans l'application et l'admin changera. Les options sont : `dev` | `staging` | `demo` | `prod`
NEWSLETTER_BREVO_LIST_ID= L'ID de la newsletter de Brevo (précedemment Send In Blue)
BREVO_API_KEY= La clé API de Brevo
SENTRY_DSN (optionnel)= Le Data Source Name pour Sentry. Peut être vide.
MATOMO_ID (optionnel)= L'ID pour le suivi avec Matomo. Compl-alim utilise l'ID 95 pour la prod, en local c'est mieux de le laisser vide
REDIS_URL= L'instance redis à utiliser pour les tâches asynchrones et le cache des clés API. Par exemple : 'redis://localhost:6379/0'
REDIS_PREPEND_KEY= Optionnel - Ajout ce string au début de chaque clé Redis. Utile pour partager la même DB Redis sur plusieurs environnements
S3CFG_FILE_URI= Optionnel - Url de téléchargement du fichier de config s3cmd
ENABLE_SILK= `True` pour activer le profiling via [django-silk](https://github.com/jazzband/django-silk) ou `False` autrement
ENABLE_AUTO_VALIDATION= `True` pour activer la validation automatique de déclarations article 15 non instruites.
INSEE_API_KEY= La clé de l'API pour l'application "API-Siren" (https://portail-api.insee.fr/). Nous avons aujourd'hui trois clés différentes pour chaque environnement : prod, staging et démo.
DATAGOUV_API_KEY=VALUE_TO_GET_FROM_DATAGOUV_ADMIN
DATAGOUV_DECLARATIONS_ID=XXXXX (can be found via data.gouv.fr's API. Other datasets can be updated. in that case you need to add DATAGOUV_<DATASET_NAME>_ID)
OBSERVATION_DAYS (optionnel)= Le nombre de jours proposé pour une période d'observation. Par défaut c'est 15.
DECLARATIONS_EXPORT_BATCH_SIZE (optionnel)= Le nombre de déclarations par batch pour l'export vers open data
DECLARATIONS_EXPORT_HOUR (optionnel)= L'heure pour l'export vers open data (par défaut c'est à 1h)
GRIST_API_KEY (optionnel)= La clé de l'API pour grist
GRIST_SD_CONTROL_DOC_ID (optionnel)= L'identifiant du document utilisé pour recuperer les mails du role contrôle. Retrouvable depuis settings -> API console de grist
GRIST_SD_CONTROL_TABLE_ID (optionnel)= L'identifiant du tableau utilisé dans GRIST_SD_CONTROL_DOC_ID. Retrouvable depuis settings -> API console de grist
GRIST_ANSES_CONTROL_DOC_ID (optionnel)= L'identifiant du document utilisé pour recuperer les mails du role contrôle. Retrouvable depuis settings -> API console de grist
GRIST_ANSES_CONTROL_TABLE_ID (optionnel)= L'identifiant du tableau utilisé dans GRIST_ANSES_CONTROL_DOC_ID. Retrouvable depuis settings -> API console de grist
ADMIN_URL (optionnel)= Permet de customiser l'URL de l'admin Django
```

#### Créer les différents modèles Django dans la base de données

```
python manage.py migrate
```

## Lancement de l'application en mode développement

Pour le développement il faudra avoir deux terminales ouvertes : une pour l'application Django, et une autre pour l'application VueJS.

### Terminal Django

Il suffit de lancer la commande Django "runserver" à la racine du projet pour avoir le serveur de développement (avec hot-reload) :

```
python manage.py runserver
```

### Terminal VueJS

Pour faire l'équivalent côté frontend, allez sur `./frontend` et lancez le serveur npm :

```
cd frontend
npm run serve
```

Une fois la compilation finie des deux côtés, l'application se trouvera sous [127.0.0.1:8000](127.0.0.1:8000) (le port Django, non pas celui de npm).

## Lancement des tests

### Lancer les tests Django

La commande pour lancer les tests Django est :

```
python manage.py test
```

Sur VSCode, ces tests peuvent être debuggés avec la configuration "Python: Tests", présente sur le menu "Run".

### Lancer les tests VueJS

Il faut d'abord se placer sur "/frontend", ensuite la commande pour lancer les tests VueJS est :

```
cd frontend
npm run test
```

## Import de données initiales (fixtures)

Pour pouvoir utiliser l'application et le backoffice avec des données proches de données réelles, il est nécessaire d'importer des données. Pour cela, vous pouvez (ce n'est pas obligatoire) importer les fixtures (données hors éléments) présentes dans le projet :

```
python manage.py myloaddata
```

Pour plus d'infos sur le fonctionnement des fixtures, [voir ce document](docs/fixtures.md)

Cela créera aussi un compte administrateur (nom d'utilisateur : `admin`, mot de passe : `azerty`).

Vous pouvez aussi créer votre propre compte administrateur avec la commande :

```
python manage.py createsuperuser
```

Pour créer autres objets rapidement, vous pouvez rentrer dans un shell `python manage.py shell` et créer des objets avec les modèles dans `data.factories`.

## Envoi des données au bucket s3 pour récupération par les serveurs

Telecharger le fichier s3cfg correspondant au bucket
```
s3cmd setpolicy ./clevercloud/allow_policy.json s3://csv-data
s3cmd put <data_directory> s3://csv-data --recursive
s3cmd setpolicy ./clevercloud/deny_policy.json s3://csv-data
```

Les serveurs d'env prod/staging/demo utilisent le script clevercloud/post_build_hook.sh pour la récupération des données

## Remplissage des champs de cache

Le modèle `Company` contient deux champs qui sont remplis via une tâche Celery :
- `market_ready_count_cache`, et
- `market_ready_count_updated_at`

Pour les remplir en local il suffit de lancer la commande `python manage.py refresh_company_cache` :

```bash
» python manage.py refresh_company_cache
Starting cache update...
2025-09-02 13:47:57,108 config.tasks INFO     Starting the cache update for market-ready declarations
2025-09-02 13:47:57,143 config.tasks INFO     Updated 7 companies (1 of 1)
2025-09-02 13:47:57,143 config.tasks INFO     Cache update done!
Synchronous cache refresh completed!
```

## Test création fichier déclarations open data

Pour tester la création du fichier de déclarations autorisées qui est envoyé à OpenData, il y a la commande

`python manage.py etl`

Il faut definir le variable d'environnement `DECLARATIONS_EXPORT_BATCH_SIZE` avant de lancer la commande.

Le fichier sera sauvegardé dans `default_storage.path("declarations.csv")`. Avec Docker en local c'est `/app/media/declarations.csv`
