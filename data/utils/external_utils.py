import logging

import datetime as dt
import requests

from data.validators import validate_siret

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

        validate_siret(siret)

        response = requests.get("https://recherche-entreprises.api.gouv.fr/search", params={"q": siret})
        if not response.ok:
            logger.warn(f"SIRET API call has failed, code {response.status_code} : {response}")
            return {"status": 500}

        formatted_company_data = SiretData.get_formatted_company_data(response.json())

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
        try:
            results = raw_siret_data["results"]
            if not results:
                return {"status": 404}
            etablissement = results[0]
            adresse = etablissement["siege"]
            cedex_items = ["cedex", "libelle_cedex"]
            address_items = [
                "numero_voie",
                "indice_repetition",
                "dernier_numero_voie",
                "type_voie",
                "libelle_voie",
            ]

            end_date = etablissement["date_fermeture"]
            # on verifie matching_etablissements parce que ça donne vraiment l'etablissement qui corresponde au SIRET donné
            # les autres infos comme siege peuvent être associées au même SIREN
            siret_matches = etablissement["matching_etablissements"]
            if not end_date and siret_matches and len(siret_matches) > 0:
                end_date = siret_matches[0]["date_fermeture"]

            return {
                "status": 200,
                "social_name": etablissement["nom_raison_sociale"] or etablissement["nom_complet"],
                "commercial_name": adresse["nom_commercial"],
                "address": " ".join(filter(None, [adresse[item] for item in address_items])),
                "additional_details": adresse["complement_adresse"],
                "city": adresse["libelle_commune"],
                "postal_code": adresse["code_postal"],
                "cedex": " ".join(filter(None, [adresse[item] for item in cedex_items])),
                "end_date": end_date,
            }
        except KeyError as e:
            safe_raw_siret_data = str(raw_siret_data).replace("\r", "").replace("\n", "")
            safe_key_error = str(e).replace("\r", "").replace("\n", "")
            logger.error(f"unexpected siret response format : {safe_raw_siret_data}. Unknown key : {safe_key_error}")
            return {"status": 500}

    @staticmethod
    def is_valid_company(company_data):
        if company_data["status"] == 404:
            return False

        end_date = company_data.get("end_date", None)
        if not end_date:
            return True

        end_date = dt.datetime.strptime(end_date, "%Y-%m-%d")
        return end_date > dt.datetime.today()
