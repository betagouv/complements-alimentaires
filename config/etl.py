import logging
from abc import ABC, abstractmethod
import json
import io
import pandas as pd
import requests
from api.views.declaration.declaration import OpenDataDeclarationsListView

logger = logging.getLogger(__name__)


def prepare_file_validata_post_request(df: pd.DataFrame):
    buffer = io.StringIO()
    df.to_csv(buffer, sep=";", index=False)
    buffer.seek(0)
    # Prepare the file for the POST request
    return {
        "file": ("data.csv", buffer, "text/csv"),
    }


class ETL(ABC):
    @abstractmethod
    def extract_dataset(self):
        pass

    @abstractmethod
    def transform_dataset(self):
        pass

    @abstractmethod
    def load_dataset(self):
        pass

    def get_schema(self):
        return self.schema

    def get_dataset(self):
        return self.df

    def len_dataset(self):
        if isinstance(self.df, pd.DataFrame):
            return len(self.df)
        else:
            return 0


class ETL_OPEN_DATA(ETL):
    def __init__(self):
        self.df = None
        self.schema = None
        self.schema_url = ""
        self.dataset_name = ""
        self.columns = []

    def _clean_dataset(self):
        self.columns = [i["name"] for i in self.schema["fields"]]

        self.df = self.df.loc[:, ~self.df.columns.duplicated()]

        self.df = self.df.reindex(self.columns, axis="columns")
        self.df.columns = self.df.columns.str.replace(".", "_")
        self.df = self.df.drop_duplicates(subset=["id"])
        self.df = self.df.reset_index(drop=True)

        for col_int in self.schema["fields"]:
            if col_int["type"] == "integer":
                # Force column o Int64 to maintain an integer column despite the NaN values
                self.df[col_int["name"]] = self.df[col_int["name"]].astype("Int64")
            if col_int["type"] == "float":
                self.df[col_int["name"]] = self.df[col_int["name"]].round(decimals=4)
        self.df = self.df.replace("<NA>", "")

    def match_to_schema_columns(self):
        self.df = self.df[self.columns]

    def is_valid(self) -> bool:
        files = prepare_file_validata_post_request(self.df)
        res = requests.post(
            "https://api.validata.etalab.studio/validate?",
            files=files,
            data={"schema": self.schema_url, "header_case": True},
        )
        report = json.loads(res.text)["report"]
        if len(report["errors"]) > 0 or report["stats"]["errors"] > 0:
            logger.error(f"The dataset {self.dataset_name} extraction has errors : ")
            logger.error(report["errors"])
            logger.error(report["tasks"])
            return False
        else:
            return True

    def _load_data_locally(self):
        self.df.to_csv("declarations.csv", sep=";", index=False)

    def load_dataset(self):
        if not self.is_valid():
            logger.error(f"The dataset {self.name} is invalid and therefore will not be exported to s3")
            return
        try:
            self._load_data_locally()
        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_DECLARATIONS(ETL_OPEN_DATA):
    def __init__(self):
        super().__init__()
        self.dataset_name = "declarations"
        self.schema = json.load(open("data/schemas/schema_declarations.json"))["schema"]
        self.schema_url = (
            "https://github.com/betagouv/complements-alimentaires/blob/staging/data/schemas/schema_declarations.json"
        )
        self.df = None
        self.columns_mapper = {
            "id": "id",
        }

    def extract_dataset(self):
        open_data_view = OpenDataDeclarationsListView()
        queryset = open_data_view.get_queryset()
        serializer = open_data_view.get_serializer_class()
        declarations = serializer(queryset, many=True).data
        self.df = pd.DataFrame(declarations)

    def transform_dataset(self):
        self._clean_dataset()
        self.match_to_schema_columns()
