import logging

import requests

logger = logging.getLogger(__name__)


class SiretData:
    """
    Permet de récupérer les données d'une entreprise à partir de l'API recherche entreprises,
    et de les formater pour les utiliser dans notre code.
    Note: la classe n'est pas instanciée et sert surtout de conteneur à la logique
    Ex d'utilisation : `SiretData.fetch("82073111500037")`
    """

    @staticmethod
    def fetch(siret: str) -> dict | None:
        """Interroge l'API SIRET, et retourne un dict contenant les attributs de l'entreprise à notre format, ou None en cas d'échec."""

        url = f"https://recherche-entreprises.api.gouv.fr/search?q={siret}"
        response = requests.get(url)
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
        'commercial_name': null,
        'address': '12 RUE DUHESME',
        'additional_details': null,
        'city': 'PARIS',
        'postal_code': '75018',
        'cedex': null}
        """
        etablissement = raw_siret_data["results"][0]
        adresse = etablissement["siege"]
        cedex_items = ["cedex", "libelle_cedex"]
        address_items = [
            "numero_voie",
            "indice_repetition",
            "dernier_numero_voie",
            "type_voie",
            "libelle_voie",
        ]

        return {
            "social_name": etablissement["nom_raison_sociale"] or etablissement["nom_complet"],
            "commercial_name": adresse["nom_commercial"],
            "address": " ".join(filter(None, [adresse[item] for item in address_items])),
            "additional_details": adresse["complement_adresse"],
            "city": adresse["libelle_commune"],
            "postal_code": adresse["code_postal"],
            "cedex": " ".join(filter(None, [adresse[item] for item in cedex_items])),
        }
