import os
import subprocess
from django.core.management.base import BaseCommand
from config.tasks import export_datasets_to_data_gouv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class Command(BaseCommand):
    help = "Export datasets to data.gouv.fr"

    def handle(self, *args, **options):
        export_datasets_to_data_gouv()
