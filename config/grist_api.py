import logging
import requests

from django.conf import settings

logger = logging.getLogger(__name__)


def fetch_control_emails_from_grist():
    sd_doc = settings.GRIST_SD_CONTROL_DOC_ID
    sd_table = settings.GRIST_SD_CONTROL_TABLE_ID
    anses_doc = settings.GRIST_ANSES_CONTROL_DOC_ID
    anses_table = settings.GRIST_ANSES_CONTROL_TABLE_ID
    if any(not env_var for env_var in [settings.GRIST_API_KEY, sd_doc, sd_table, anses_doc, anses_table]):
        raise Exception(
            "GRIST_API_KEY, GRIST_SD_CONTROL_DOC_ID, GRIST_SD_CONTROL_TABLE_ID, GRIST_ANSES_CONTROL_DOC_ID, GRIST_ANSES_CONTROL_TABLE_ID must all be defined to fetch emails"
        )
    header = {"Authorization": f"Bearer {settings.GRIST_API_KEY}"}
    response = requests.get(
        f"https://grist.numerique.gouv.fr/api/docs/{sd_doc}/tables/{sd_table}/records", headers=header
    )
    response.raise_for_status()
    records = response.json()["records"]
    logger.info(f"{len(records)} records imported from SD table")
    response = requests.get(
        f"https://grist.numerique.gouv.fr/api/docs/{anses_doc}/tables/{anses_table}/records", headers=header
    )
    response.raise_for_status()
    anses_records = response.json()["records"]
    logger.info(f"{len(anses_records)} records imported from ANSES table")
    records += anses_records
    return [r["fields"]["mail"] for r in records]
