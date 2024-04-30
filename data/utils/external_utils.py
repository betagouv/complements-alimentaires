import logging

from django.conf import settings

import requests

from tokens.models import InseeToken

logger = logging.getLogger(__name__)


class SiretData:
    """
    Permet de récupérer les données d'une entreprise à partir de l'API INSEE, et de les formater pour les utiliser dans notre code.
    Note: la classe n'est pas instanciée et sert surtout de conteneur à la logique
    Ex d'utilisation : `SiretData.fetch("82073111500037")`
    """

    @staticmethod
    def fetch(siret: str) -> dict | None:
        """Interroge l'API SIRET, et retourne un dict contenant les attributs de l'entreprise à notre format, ou None en cas d'échec."""

        insee_token = InseeToken.load()  # créé ou récupère (et met à jour si besoin) un token de connexion
        if not insee_token.usable:
            logger.warn("SIRET API won't be called as no INSEE token can't be used for now")
            return None

        url = settings.INSEE_SIRET_API_URL + siret
        response = requests.get(url, headers={"Authorization": f"Bearer {insee_token.key}"})
        if not response.ok:
            logger.warn(f"SIRET API call has failed, code {response.status_code} : {response}")
            return None

        try:
            formatted_company_data = SiretData.get_formatted_company_data(response.json())
        except KeyError as e:
            logger.warn(f"unexpected siret response format : {response}. Unknown key : {e}")
            return None

        return formatted_company_data

    @staticmethod
    def get_formatted_company_data(raw_siret_data: dict) -> dict:
        """
        Transforme une réponse brute de l'API SIRET en dictionnaire d'attributs utilisables pour instancier une `Company`.
        Exemple de retour :
        {'social_name': 'TOO GOOD TO GO FRANCE',
        'address': '12 RUE DUHESME',
        'city': 'PARIS',
        'postal_code': '75018',
        'cedex': ''}
        """

        etablissement = raw_siret_data["etablissement"]
        adresse = etablissement["adresseEtablissement"]
        cedex_items = ["codeCedexEtablissement", "libelleCedexEtablissement"]
        address_items = [
            "complementAdresseEtablissement",
            "numeroVoieEtablissement",
            "indiceRepetitionEtablissement",
            "dernierNumeroVoieEtablissement",
            "indiceRepetitionDernierNumeroVoieEtablissement",
            "typeVoieEtablissement",
            "libelleVoieEtablissement",
        ]

        return {
            "social_name": etablissement["uniteLegale"]["denominationUniteLegale"],
            "address": " ".join(filter(None, [adresse[item] for item in address_items])),
            "city": adresse["libelleCommuneEtablissement"],
            "postal_code": etablissement["adresseEtablissement"]["codePostalEtablissement"],
            "cedex": " ".join(filter(None, [adresse[item] for item in cedex_items])),
        }
