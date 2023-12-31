# Compléments Alimentaires

Projet en construction

### À installer localement

- [Python3](https://www.python.org/downloads/) (de préference 3.8)
- [pip](https://pip.pypa.io/en/stable/installing/) (souvent installé avec Python)
- [vitrualenv](https://virtualenv.pypa.io/en/stable/installation.html)
- [Node et npm](https://nodejs.org/en/download/)
- [Postgres](https://www.postgresql.org/download/)
- [pre-commit](https://pypi.org/project/pre-commit/)

### Création d'un environnement Python3 virtualenv

Pour commencer, c'est recommandé de créer un environnement virtuel avec Python3.

```
virtualenv -p python3 venv
source ./venv/bin/activate
```

### Installer les dépendances du backend

Les dépendances du backend se trouvent dans `requirements.txt`. Pour les installer :

```
pip install -r requirements.txt
```

### Installer les dépendances du frontend

On utilise les dernires versions LTS de `node` et `npm`.

L'application frontend se trouve sous `/frontend`. Pour installer les dépendances :

```
cd frontend
npm install
```

### Créer la base de données

Par exemple, pour utiliser une base de données nommée _icare_ :

```
createdb icare
```
Le user doit avoir les droits de creation

```
sudo su postgres
postgres=# create user <DB_USER> createdb password <DB_PASSWORD>;
```

### Compléter les variables d'environnement

L'application utilise [python-dotenv](https://pypi.org/project/python-dotenv/), vous pouvez donc créer un fichier `.env` à la racine du projet avec ces variables définies :

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
```

## Lancer l'application en mode développement

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

### Pre-commit

On utilise l'outil [`pre-commit`](https://pre-commit.com/) pour effectuer des vérifications automatiques
avant chaque commit. Cela permet par exemple de linter les code Python, Javascript et HTML.

Pour pouvoir l'utiliser, il faut installer `pre-commit` (en général plutôt de manière globable que dans
l'environnement virtuel) : `pip install pre-commit`.

Puis l'activer : `pre-commit install`.

Les vérifications seront ensuite effectuées avant chaque commit. Attention, lorsqu'une vérification `fail`,
le commit est annulé. Il faut donc que toutes les vérifications passent pour que le commit soit pris en
compte. Si exceptionnellement vous voulez commiter malgré qu'une vérification ne passe pas, c'est possible
avec `git commit -m 'my message' --no-verify`.

## Lancer les tests pour l'application Django

La commande pour lancer les tests Django est :

```
python manage.py test
```

Sur VSCode, ces tests peuvent être debuggés avec la configuration "Python: Tests", présente sur le menu "Run".

## Lancer les tests pour l'application VueJS

Il faut d'abord se placer sur "/frontend", ensuite la commande pour lancer les tests VueJS est :

```
cd frontend
npm run test
```

## Creation d'un superuser

Afin de pouvoir s'identifier dans le backoffice (sous /admin), il est nécessaire de créer un utilisateur admin avec tous les droits. Pour ce faire, vous pouvez en console lancer :

```
python manage.py createsuperuser
```

## Import de données dans les tables ingrédient

Pour pouvoir tester l'application et le backoffice avec des données réelles, il est nécessaire d'importer des données. Pour cela :
```
python manage.py load_ingredients
```
