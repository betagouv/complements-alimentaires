import csv
from django.core.files.storage import default_storage
from django.core.paginator import Paginator
import json
import logging
import pandas as pd

from . import datagouv

from api.serializers import OpenDataDeclarationSerializer
from data.models import Declaration

logger = logging.getLogger(__name__)


class OpenDataDeclarationsETL:
    def __init__(self):
        super().__init__()
        self.dataset_name = "declarations"
        self.schema = json.load(open("data/schemas/schema_declarations.json"))
        # self.schema_url = "https://raw.githubusercontent.com/betagouv/complements-alimentaires/refs/heads/main/data/schemas/schema_declarations.json"
        self.columns = [i["name"] for i in self.schema["fields"]]
        self.serializer = OpenDataDeclarationSerializer
        self.queryset = Declaration.objects.filter(status=Declaration.DeclarationStatus.AUTHORIZED).order_by(
            "-modification_date"
        )
        self.filename = f"{self.dataset_name}.csv"

        # supprimer l'ancien fichier pour preparer l'action d'append du load_dataframe
        if default_storage.exists(self.filename):
            default_storage.delete(self.filename)

    def export(self, batch_size):
        # TODO: try/except at each stage in the process? For fine grained debugging
        # alternatively, try/except within processes, raising errors with extra info on what step we're at
        paginated_queryset = self.extract_paginated_queryset(batch_size)
        for page_num in paginated_queryset.page_range:
            page_queryset = paginated_queryset.page(page_num).object_list
            batched_df = self.transform_queryset(page_queryset)
            self.load_dataframe(batched_df)
        # TODO: log?

    def extract_paginated_queryset(self, batch_size):
        return Paginator(self.queryset, batch_size)

    # cette méthode prend un queryset et redonne un pandas dataframe
    def transform_queryset(self, queryset):
        queryset = self.serializer.setup_eager_loading(queryset)
        serialized_queryset = self.serializer(queryset, many=True).data

        dataframe = pd.DataFrame(serialized_queryset)
        # spécifier l'ordre de colonnes
        dataframe = dataframe[self.columns]
        dataframe = dataframe.replace({"\n": " ", "\r": " "}, regex=True)

        # transforme les objects en json strings pour éviter de créer un csv avec des json string
        # qui ne respectent pas https://www.rfc-editor.org/rfc/rfc7159#section-7
        json_columns = dataframe.columns[dataframe.map(type).eq(list).any()]
        dataframe[json_columns] = (
            dataframe[json_columns].map(lambda x: json.dumps(x, ensure_ascii=False)).astype("string")
        )

        return dataframe

    # sauvegarder le dataframe dans le fichier pour l'export
    def load_dataframe(self, dataframe):
        file_exists = default_storage.exists(self.filename)
        with default_storage.open(self.filename, "a") as csv_file:
            dataframe.to_csv(
                csv_file,
                header=not file_exists,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONNUMERIC,
                escapechar="\\",
                date_format="%Y-%m-%d",
            )

    def publish(self):
        datagouv.update_resources(self.dataset_name)
