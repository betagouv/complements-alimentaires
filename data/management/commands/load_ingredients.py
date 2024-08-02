import datetime
import logging
import os

from django.core.management.base import BaseCommand

from data.etl.csv_importer import import_csv_from_filepath
from data.exceptions import CSVFileError
from data.models.plant import Part

logger = logging.getLogger(__name__)


def check_for_incomplete_data(model):
    incomplete_objects = model.objects.filter(name="")
    incomplete_objects.update(missing_import_data=True)
    logger.info(f"{len(incomplete_objects)} instance(s) de {model.__name__} incomplete(s).")


class Command(BaseCommand):
    help = "Load the ingredients from the csv files given by SICCRF"

    def add_arguments(self, parser):
        parser.add_argument(
            "date",
            type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
            help="Indique la date d'export.",
        )
        # argument optionnel
        parser.add_argument(
            "-d",
            "--directory",
            type=str,
            help="Indique où les fichiers d'export se trouvent.",
            default="files",
        )

    def handle(self, *args, **options):
        directory_relative_path = options.get("directory")
        files = os.listdir(directory_relative_path)
        export_date = options.get("date")
        models_to_check = set()
        for file in files:
            try:
                updated_models = import_csv_from_filepath(os.path.join(directory_relative_path, file), export_date)
                models_to_check = models_to_check.union(updated_models)
            except CSVFileError as e:
                logger.error(e.message)

        for model in models_to_check:
            if model != Part:
                check_for_incomplete_data(model)
