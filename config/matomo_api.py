import logging

from django.conf import settings

import requests

logger = logging.getLogger(__name__)


class MatomoAPI:
    def __init__(self):
        self.base_url = "https://stats.beta.gouv.fr"
        self.site_id = settings.MATOMO_ID or "95"  # Les environnements prod et démo utiliseront l'ID 95

    def _make_request(self, params):
        query_params = {
            "idSite": self.site_id,
            "format": "json",
            **params,
        }

        try:
            response = requests.get(f"{self.base_url}/index.php", params=query_params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            return None

    def get_page_evolution(self, period="month", date="previous6", metric="nb_visits", label="element"):
        """Obtient l'évolution des visites d'une page en particulier"""
        data = self._make_request(
            {
                "module": "API",
                "method": "API.getRowEvolution",
                "period": period,
                "date": date,
                "label": label,
                "metric": metric,
                "apiModule": "Actions",
                "apiAction": "getPageUrls",
            },
        )
        if data and data["reportData"]:
            reformatted_report_data = {}
            for month, value in data["reportData"].items():
                reformatted_report_data[month] = value[0]
            data["reportData"] = reformatted_report_data

        return data

    def get_version(self):
        """Obtient la version Matomo"""
        return self._make_request({"method": "getMatomoVersion"})
