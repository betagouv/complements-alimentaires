import logging
import os

from django.core.management.base import BaseCommand

from data.csv_importer import import_csv
from data.exceptions import CSVFileError

logger = logging.getLogger(__name__)


def check_for_incomplete_data(model):
    incomplete_objects = model.objects.filter(name="")
    incomplete_objects.update(missing_import_data=True)
    logger.info(f"{len(incomplete_objects)} {model} sont incomplets")


class Command(BaseCommand):
    help = "Load the ingredients from the csv files given by SICCRF"

    def add_arguments(self, parser):
        # argument optionnel
        parser.add_argument(
            "-d", "--directory", type=str, help="Indicates where the files are located.", default="files"
        )

    def handle(self, *args, **options):
        directory_relative_path = options.get("directory")
        files = os.listdir(directory_relative_path)
        models_to_check = set()
        for file in files:
            try:
                updated_models = import_csv(os.path.join(directory_relative_path, file))
                models_to_check = models_to_check.union(updated_models)
            except CSVFileError as e:
                logger.error(e.message)

        for model in models_to_check:
            check_for_incomplete_data(model)
