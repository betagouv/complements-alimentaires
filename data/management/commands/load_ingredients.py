from django.core.management.base import BaseCommand

from data.csv_importer import import_csv

import os


class Command(BaseCommand):
    help = "Load the ingredients from the csv files given by SICCRF"

    def handle(self, *args, **options):
        files = os.listdir("files")
        for file in files:
            import_csv(os.path.join("files", file))
