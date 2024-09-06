import os
import subprocess

from django.core.management.base import BaseCommand

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class Command(BaseCommand):
    help = "Exports poetry dependencies to requirements.txt"

    def handle(self, *args, **options):
        subprocess.run(
            [
                "poetry",
                "export",
                "-o",
                "requirements.txt",
                "--without-hashes",
            ]
        )
