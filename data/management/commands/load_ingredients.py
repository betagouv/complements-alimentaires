import datetime
import logging
import os

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from data.etl.exceptions import CSVFileError
from data.etl.teleicare_ingredients.csv_importer import import_csv_from_filepath
from data.etl.teleicare_ingredients.post_load_transformation import deduplicate_substances_ingredients

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load the ingredients from the csv files given by SICCRF"
    _start_time = None

    def elapsed_time(self):
        if self._start_time is None:
            return None
        return timezone.now() - self._start_time

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
        try:
            with transaction.atomic():
                logger.info("Début de l'import des csv de référe ce de TeleIcare et déduplication\n")
                self._start_time = timezone.now()

                directory_relative_path = options.get("directory")
                files = os.listdir(directory_relative_path)
                export_date = options.get("date")
                models_to_check = set()
                # load et transform fichier par fichier
                for file in files:
                    try:
                        updated_models = import_csv_from_filepath(
                            os.path.join(directory_relative_path, file), export_date
                        )
                        models_to_check = models_to_check.union(updated_models)
                    except CSVFileError as e:
                        logger.error(e.message)

                # transform une fois tous les fichiers importés
                deduplicate_substances_ingredients()

                logger.info(f"Import et déduplication executées en {self.elapsed_time()}\n")
        except Exception as e:  # noqa
            logger.exception(e)
            raise CommandError(
                "Une exception imprévue est arrivée. L'import et la déduplication ont avorté, l'état de la base de données reste inchangé\n"
            )
