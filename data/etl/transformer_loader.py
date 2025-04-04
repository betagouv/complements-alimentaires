import csv
import json
import logging

from django.core.files.storage import default_storage

from data.etl import datagouv

from .extractor import DECLARATIONS, TRANSFORMER_LOADER

logger = logging.getLogger(__name__)


class OPEN_DATA(TRANSFORMER_LOADER):
    """
    Abstract class implementing the specifity for open data export
    """

    def _load_data_csv(self, filename):
        df_csv = self.df.copy()

        # transforme les objects en json strings pour éviter de créer un csv avec des json string
        # qui ne respectent pas https://www.rfc-editor.org/rfc/rfc7159#section-7
        json_columns = self.df.columns[self.df.applymap(type).eq(list).any()]
        self.df[json_columns] = self.df[json_columns].map(json.dumps).astype("string")

        with default_storage.open(filename + ".csv", "w") as csv_file:
            df_csv.to_csv(
                csv_file,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONNUMERIC,
                escapechar="\\",
                date_format="%Y-%m-%d",
            )

    def load_dataset(self):
        filepath = f"{self.dataset_name}"
        # TODO : traitement par batch pour permettre la validation par Validata
        # if not self.is_valid():
        #     logger.error(f"The dataset {self.dataset_name} is invalid and therefore will not be exported to s3")
        #     return
        try:
            self._load_data_csv(filepath)
            datagouv.update_resources(self.dataset_name)

        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_DECLARATIONS(DECLARATIONS, OPEN_DATA):
    def transform_dataset(self):
        self.clean_dataset()
