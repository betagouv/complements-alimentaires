from django.core.management.base import BaseCommand

from data.csv_importer import import_csv

import os


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
        for file in files:
            import_csv(os.path.join(directory_relative_path, file))
