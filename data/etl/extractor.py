import csv
import io
import json
import logging
from abc import ABC, abstractmethod

import pandas as pd
import requests

from api.views.declaration.declaration import OpenDataDeclarationsListView

logger = logging.getLogger(__name__)

# ---------------- utils functions ----------------------


def prepare_file_validata_post_request(df: pd.DataFrame):
    """
    Prepare a pandas Dataframe in order to be sent via a API Post request using the param "files"
    """
    buffer = io.StringIO()
    # df.to_csv(buffer, sep=";", index=False)
    df.to_csv(
        buffer,
        sep=";",
        index=False,
        na_rep="",
        encoding="utf_8_sig",
        quoting=csv.QUOTE_NONNUMERIC,
        escapechar="\\",
        date_format="%Y-%m-%d",
    )
    buffer.seek(0)
    return {
        "file": ("data.csv", buffer, "text/csv"),
    }


# -------------------- ETL classes ----------------------
class ETL(ABC):
    def __init__(self):
        self.df = None
        self.schema = None
        self.schema_url = ""
        self.dataset_name = ""
        self.columns = []

    def get_schema(self):
        return self.schema

    def get_dataset(self):
        return self.df

    def len_dataset(self):
        if isinstance(self.df, pd.DataFrame):
            return len(self.df)
        else:
            return 0

    def clean_dataset(self):
        self.df = self.df.loc[:, ~self.df.columns.duplicated()]
        ## Code temporaire en attendant d'avoir tous les champs du schéma
        columns_to_keep = []
        for col in self.columns:
            if col in self.df.columns:
                columns_to_keep.append(col)
        # ---------------------------------------------------
        self.df = self.df[columns_to_keep]
        self.df = self.df.replace({"\n": " ", "\r": " "}, regex=True)

    # Cette méthode n'est pas appelé actuellement
    # La taille max de fichier acceptable par l'api validata est 10Mo
    # Nos fichiers font ~ 50 Mo
    def is_valid(self) -> bool:
        files = prepare_file_validata_post_request(self.df)
        res = requests.post(
            "https://api.validata.etalab.studio/validate?",
            files=files,
            data={"schema": self.schema_url, "header_case": True},
        )
        try:
            report = json.loads(res.text)["report"]
        except json.decoder.JSONDecodeError as err:
            logger.error(f"Erreur {err} en decodant : {res.text}")
            return False
        if len(report["errors"]) > 0 or report["stats"]["errors"] > 0:
            logger.error(f"The dataset {self.dataset_name} extraction has errors : ")
            logger.error(report["errors"])
            logger.error(report["tasks"])
            return False
        else:
            return True


class EXTRACTOR(ETL):
    @abstractmethod
    def extract_dataset(self):
        pass


class TRANSFORMER_LOADER(ETL):
    @abstractmethod
    def transform_dataset(self):
        pass

    @abstractmethod
    def load_dataset(self):
        pass


class DECLARATIONS(EXTRACTOR):
    def __init__(self):
        super().__init__()
        self.dataset_name = "declarations"
        self.schema = json.load(open("data/schemas/schema_declarations.json"))
        self.schema_url = "https://raw.githubusercontent.com/betagouv/complements-alimentaires/refs/heads/main/data/schemas/schema_declarations.json"
        self.df = None
        self.columns = [i["name"] for i in self.schema["fields"]]

    def extract_dataset(self):
        open_data_view = OpenDataDeclarationsListView()
        queryset = open_data_view.get_queryset()
        serializer = open_data_view.get_serializer_class()
        declarations = serializer(queryset, many=True).data
        self.df = pd.DataFrame(declarations)
