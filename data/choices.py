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
