import csv
import logging
import requests

logger = logging.getLogger(__name__)


class DataGouvAPI:
    def __init__(self):
        self.base_csv_url = "https://metric-api.data.gouv.fr/api/datasets/data/csv"
        self.declaration_data_set_id = "67484631f54100f9e9db2a06"
        # "https://metric-api.data.gouv.fr/api/datasets/data/csv/?metric_month__sort=asc&dataset_id__exact=584ecf1ac751df202dc0bb7e" old

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

    def get_declaration_stats(self):
        url = f"{self.base_csv_url}/?metric_month__sort=asc&dataset_id__exact={self.declaration_data_set_id}"
        stats_list = self._make_csv_request(url)
        report_data = {}
        for stat in stats_list:
            if stat[0] == "__id":
                continue
            print(stat)
            report_data[stat[2]] = {"visits": stat[3], "downloads": stat[4]}
        return {"reportData": report_data}
