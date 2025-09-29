import requests

from django.conf import settings


def fetch_control_emails_from_grist():
    if not settings.GRIST_API_KEY:
        raise Exception("GRIST_API_KEY not set")
    header = {"Authorization": f"Bearer {settings.GRIST_API_KEY}"}
    response = requests.get(
        "https://grist.numerique.gouv.fr/api/docs/xAQvnUyC2QEok7c8Yvqw6x/tables/Table1/records", headers=header
    )
    response.raise_for_status()
    records = response.json()["records"]
    return [r["fields"]["mail"] for r in records]
