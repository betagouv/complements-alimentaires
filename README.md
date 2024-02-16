# Compléments Alimentaires

_Projet en construction_

## Installation du projet

Il existe 2 méthodes distinctes d'installation pour ce projet :
1) l'installation manuelle classique
2) l'installation automatique via un [devcontainer](https://code.visualstudio.com/docs/devcontainers/containers) (nécessite Docker et VS Code)


### Installation manuelle classique (_méthode 1_)


#### À installer localement

- [Python3](https://www.python.org/downloads/) (version 3.11)
- [poetry](https://pip.pypa.io/en/stable/installing/) (`pip install poetry==1.7.1`)
- [Node et npm](https://nodejs.org/en/download/) (version 20 LTS)
- [Postgres](https://www.postgresql.org/download/) (version 15)

#### Installer les dépendances du backend

Pour installer les dépendances du backend :

```
poetry install --no-root
```

Cette action créera aussi un environnement virtuel automatiquement. Il n'est donc pas nécessaire d'utiliser un autre outil tel que virtualenv.

#### Installer les dépendances du frontend

L'application frontend se trouve sous `/frontend`. Pour installer les dépendances :

```
cd frontend
npm install
```

#### Créer la base de données

Par exemple, pour utiliser une base de données nommée _icare_ :

```
createdb icare
```
Le user doit avoir les droits de creation

```
sudo su postgres
postgres=# create user <DB_USER> createdb password <DB_PASSWORD>;
```

#### Pre-commit

On utilise l'outil [`pre-commit`](https://pre-commit.com/) pour effectuer des vérifications automatiques
avant chaque commit. Cela permet par exemple de linter les code Python, Javascript et HTML.

Pour pouvoir l'utiliser, il faut l'activer : `pre-commit install`.

Les vérifications seront ensuite effectuées avant chaque commit. Attention, lorsqu'une vérification `fail`,
le commit est annulé. Il faut donc que toutes les vérifications passent pour que le commit soit pris en
compte. Si exceptionnellement vous voulez commiter malgré qu'une vérification ne passe pas, c'est possible
avec `git commit -m 'my message' --no-verify`.


### Installation automatique via un devcontainer (_méthode 2_)

- Installer [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Installer l'extension [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) dans VS Code
- Dans VS Code, lancer la commande `Clone Repository in Container Volume` et suivre les instructions. Le container va alors être créé.
- Une fois le container créé, si une icône de chargement reste présente sur l'icône des extensions dans le menu gauche (bug VS Code), lancer la commande `Reload Window` pour régler le soucis.

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

## Création / import de données initiales

#### Creation d'un superuser

Afin de pouvoir s'identifier dans le backoffice (sous /admin), il est nécessaire de créer un utilisateur admin avec tous les droits. Pour ce faire, vous pouvez en console lancer :

```
python manage.py createsuperuser
```

#### Import de données dans les tables ingrédient

Pour pouvoir tester l'application et le backoffice avec des données réelles, il est nécessaire d'importer des données. Pour cela :
```
python manage.py load_ingredients
```
