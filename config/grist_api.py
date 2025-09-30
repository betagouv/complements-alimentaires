import requests

from django.conf import settings


def fetch_control_emails_from_grist():
    grist_doc = settings.GRIST_CONTROL_DOC_ID
    grist_table = settings.GRIST_CONTROL_TABLE_ID
    if not settings.GRIST_API_KEY or not grist_doc or not grist_table:
        raise Exception(
            "GRIST_API_KEY, GRIST_CONTROL_DOC_ID, and GRIST_CONTROL_TABLE_ID must all be defined to fetch emails"
        )
    header = {"Authorization": f"Bearer {settings.GRIST_API_KEY}"}
    response = requests.get(
        f"https://grist.numerique.gouv.fr/api/docs/{grist_doc}/tables/{grist_table}/records", headers=header
    )
    response.raise_for_status()
    records = response.json()["records"]
    return [r["fields"]["mail"] for r in records]
