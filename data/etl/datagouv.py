import os
import logging
import requests
from datetime import date


logger = logging.getLogger(__name__)


def update_resources(dataset_name: str):
    """
    Updating the URL of the different resources dsiplayed on data.gouv.fr in order to force their cache reload and display the correct update dates
    Must have environnement variables specified :

    * ENVIRONNEMENT=prod (not updating the ressource in dev/staging environment)
    * DATAGOUV_API_KEY=VALUE_TO_GET_FROM_DATAGOUV_ADMIN
    * DATAGOUV_<DATASET_NAME>_ID=3f73d129-6b24-45cd-95e9-9bacc216d9d9  (exemple : DATAGOUV_DECLARATIONS_ID, can be found via data.gouv.fr's API)

    Returns : Number of updated resources
    """
    if os.environ.get("ENVIRONMENT") != "prod":
        return
    dataset_id = os.getenv(f"DATAGOUV_{dataset_name.upper()}_ID", "")
    api_key = os.getenv("DATAGOUV_API_KEY", "")
    if not (dataset_id and api_key):
        logger.error("Datagouv resource update : API key or dataset id incorrect values")
        return
    header = {"X-API-KEY": api_key}
    try:
        response = requests.get(f"https://www.data.gouv.fr/api/1/datasets/{dataset_id}", headers=header)
        response.raise_for_status()
        resources = response.json()["resources"]
        count_updated_resources = 0
        for resource in resources:
            if resource["format"] in ["csv"]:
                today = date.today()
                updated_url = resource["url"].split("?")[0] + "?v=" + today.strftime("%Y%m%d")
                response = requests.put(
                    f'https://www.data.gouv.fr/api/1/datasets/{dataset_id}/resources/{resource["id"]}',
                    headers=header,
                    json={"url": updated_url},
                )
                response.raise_for_status()
                count_updated_resources += 1
        return count_updated_resources
    except requests.HTTPError as e:
        logger.error(f"Datagouv resource update : Error while updating dataset : {dataset_id}")
        logger.exception(e)
    except Exception as e:
        logger.exception(e)
