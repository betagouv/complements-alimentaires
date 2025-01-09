import csv
import os
import logging

from django.core.files.storage import default_storage
from .extractor import TRANSFORMER_LOADER, DECLARATIONS

logger = logging.getLogger(__name__)


class OPEN_DATA(TRANSFORMER_LOADER):
    """
    Abstract class implementing the specifity for open data export
    """

    def _load_data_csv(self, filename):
        df_csv = self.df.copy()
        with default_storage.open(filename + ".csv", "w") as csv_file:
            df_csv.to_csv(
                csv_file,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONE,
                escapechar="\\",
            )

    def load_dataset(self):
        filepath = f"{self.dataset_name}"
        if (
            os.environ.get("STATICFILES_STORAGE") == "dstorages.backends.s3boto3.S3StaticStorage"
            and os.environ.get("DEFAULT_FILE_STORAGE") == "storages.backends.s3boto3.S3Boto3Storage"
        ):
            if not self.is_valid():
                logger.error(f"The dataset {self.name} is invalid and therefore will not be exported to s3")
                return
        try:
            self._load_data_csv(filepath)

        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_DECLARATIONS(DECLARATIONS, OPEN_DATA):
    def __init__(self):
        super().__init__()
        self.columns_mapper = {
            "id": "id",
            "status": "decision",
            "name": "nom_commercial",
            "brand": "marque",
            "gamme": "gamme",
            "article": "article_reference",
            "galenic_formulation": "forme_galenique",
            "daily_recommended_dose": "dose_journaliere",
            "instructions": "mode_emploi",
            "warning": "mises_en_garde",
            "effects": "objectif_effet",
            "flavor": "aromes",
            "conditions_not_recommended": "facteurs_risques",
            "populations": "populations_cibles",
            "declared_plants": "plantes",
            "declared_microorganisms": "micro_organismes",
            "declared_substances": "substances",
            "modification_date": "date_decision",  #  Warning : Se baser sur la du snapshot d'autorisation si la plateforme Compl'Alim permet d'editer la déclaration (ex: abandon)
        }

    def transform_dataset(self):
        self.df = self.df.rename(columns=self.columns_mapper)
        self.df["responsable_mise_sur_marche"] = self.df["company"].apply(lambda x: x[0])
        self.df["siret_responsable_mise_sur_marche"] = self.df["company"].apply(lambda x: x[1])
        self.clean_dataset()
