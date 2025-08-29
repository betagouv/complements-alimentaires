from django.db import models


class CountryChoices(models.TextChoices):
    """
    Each country is represented by a two-letter country code (ISO 3166-1 alpha-2) and its name in French.
    Note that "Irlande du Nord" does not have an official ISO country code because it is part of the United Kingdom.
    """

    FRANCE = "FR", "France"
    GERMANY = "DE", "Allemagne"
    AUSTRIA = "AT", "Autriche"
    BELGIUM = "BE", "Belgique"
    BULGARIA = "BG", "Bulgarie"
    CYPRUS = "CY", "Chypre"
    CROATIA = "HR", "Croatie"
    DENMARK = "DK", "Danemark"
    SPAIN = "ES", "Espagne"
    ESTONIA = "EE", "Estonie"
    FINLAND = "FI", "Finlande"
    GREECE = "GR", "Grèce"
    HUNGARY = "HU", "Hongrie"
    IRELAND = "IE", "Irlande"
    NORTHERN_IRELAND = "NI", "Irlande du Nord"  # NI is not an official ISO code
    ICELAND = "IS", "Islande"
    ITALY = "IT", "Italie"
    LATVIA = "LV", "Lettonie"
    LIECHTENSTEIN = "LI", "Liechtenstein"
    LITHUANIA = "LT", "Lituanie"
    LUXEMBOURG = "LU", "Luxembourg"
    MALTA = "MT", "Malte"
    NORWAY = "NO", "Norvège"
    NETHERLANDS = "NL", "Pays-Bas"
    POLAND = "PL", "Pologne"
    PORTUGAL = "PT", "Portugal"
    ROMANIA = "RO", "Roumanie"
    SLOVAKIA = "SK", "Slovaquie"
    SLOVENIA = "SI", "Slovénie"
    SWEDEN = "SE", "Suède"
    CZECH_REPUBLIC = "CZ", "République Tchèque"


class FrAuthorizationReasons(models.TextChoices):
    TRADITIONAL_USAGE = (
        "TRADITIONAL_USAGE",
        "Ingrédient bénéficiant d'un historique de consommation selon le catalogue Novel Food ou dont l'utilisation en alimentation humaine est bien établie",
    )
    NOVEL_FOOD = (
        "NOVEL_FOOD",
        "L'ingrédient figure sur la liste de l'Union des nouveaux aliments conformément au règlement (UE) 2017/2470",
    )
    MISSING = "MISSING", "L'ingrédient est autorisé en France mais ne figure pas dans la base de données"


class AuthorizationModes(models.TextChoices):
    FR = "FR", "Utilisable en France"
    EU = "EU", "Autorisé dans un État membre de l'UE ou EEE"


class IngredientActivity(models.IntegerChoices):
    """
    Les activités sont des IntegerChoices, car les Integer choisis pour chaque choix sont utilisés comme id dans les tables SICCRF
    Ce sont des équivalents de siccrf_id, qu'il ne faut donc pas modifier si on veut s'assurer de la cohérence des données.
    """

    ACTIVE = 1, "actif"
    NOT_ACTIVE = 0, "non actif"
