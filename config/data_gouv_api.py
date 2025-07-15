import csv
import logging

import requests

logger = logging.getLogger(__name__)


class DataGouvAPI:
    def __init__(self):
        self.base_csv_url = "https://metric-api.data.gouv.fr/api/datasets/data/csv"
        self.declaration_data_set_id = "67484631f54100f9e9db2a06"

    def _make_csv_request(self, url):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.exception(e)
            return []

        decoded_content = response.content.decode("utf-8")

        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        return list(cr)

    def _format_visit_stats(self, stats_list):
        report_data = {}
        for stat in stats_list:
            if stat[0] == "__id":
                continue
            report_data[stat[2]] = {"visits": stat[3], "downloads": stat[4]}
        return report_data

    def get_declaration_stats(self):
        url = f"{self.base_csv_url}/?metric_month__sort=asc&dataset_id__exact={self.declaration_data_set_id}"
        stats_list = self._make_csv_request(url)
        return {"reportData": self._format_visit_stats(stats_list)}
