import logging
from abc import ABC, abstractmethod
import json
import pandas as pd
from api.views.declaration.declaration import OpenDataDeclarationsListView

logger = logging.getLogger(__name__)


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
        return True

    def _load_data_data_gouv(self):
        self.df.to_csv("open_data.csv", sep=";", index=False)

    def load_dataset(self):
        if not self.is_valid():
            logger.error(f"The dataset {self.name} is invalid and therefore will not be exported to s3")
            return
        try:
            self._load_data_data_gouv()
        except Exception as e:
            logger.error(f"Error saving validated data: {e}")


class ETL_OPEN_DATA_DECLARATIONS(ETL_OPEN_DATA):
    def __init__(self):
        super().__init__()
        self.dataset_name = "declarations"
        self.schema = json.load(open("data/schemas/schema_declarations.json"))["schema"]
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
