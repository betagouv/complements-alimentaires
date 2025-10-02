import csv
from django.conf import settings
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
        self.dataset_name = settings.DECLARATIONS_EXPORT_DATASET_NAME
        self.schema = json.load(open("data/schemas/schema_declarations.json"))
        self.columns = [i["name"] for i in self.schema["fields"]]
        self.serializer = OpenDataDeclarationSerializer
        self.queryset = Declaration.objects.filter(status=Declaration.DeclarationStatus.AUTHORIZED).order_by(
            "-modification_date"
        )
        self.filename = f"{self.dataset_name}.csv"

    def export(self):
        logger.info("OpenDataDeclarationsETL: Starting export")
        paginated_queryset = self.extract_paginated_queryset()
        logger.info(f"OpenDataDeclarationsETL: {paginated_queryset.num_pages} batches to process")
        all_dfs = []
        for page_num in paginated_queryset.page_range:
            page_queryset = paginated_queryset.page(page_num).object_list
            all_dfs.append(self.transform_queryset(page_queryset))
            logger.info(f"OpenDataDeclarationsETL: batch {page_num} transformed")
        logger.info("OpenDataDeclarationsETL: Starting write to CSV")
        # faire la concatenation à la fin pour le rendement
        # https://stackoverflow.com/a/39815686/3845770
        complete_df = pd.concat(all_dfs)
        self.load_dataframe(complete_df)
        logger.info("OpenDataDeclarationsETL: Export completed")

    def extract_paginated_queryset(self):
        batch_size = settings.DECLARATIONS_EXPORT_BATCH_SIZE
        if not batch_size:
            raise Exception("DECLARATIONS_EXPORT_BATCH_SIZE must be defined as an environment variable")
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
        with default_storage.open(self.filename, "w") as csv_file:
            dataframe.to_csv(
                csv_file,
                header=True,
                sep=";",
                index=False,
                na_rep="",
                encoding="utf_8_sig",
                quoting=csv.QUOTE_NONNUMERIC,
                escapechar="\\",
                date_format="%Y-%m-%d",
            )

    def publish(self):
        if self.dataset_name == "declarations":
            datagouv.update_resources(self.dataset_name)
        # si le nom n'est pas "declarations", c'est pour debugger l'export
        # et alors on ne veut pas publier les résultats
