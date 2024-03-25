from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from data.utils.shell_utils import yes_or_no
from .utils import get_model_path, get_models, get_full_path


class Command(BaseCommand):
    help = """Slight wrapper around orginal dumpdata command to:
    - have default parameters
    - have a confirmation prompt
    - create 1 file per model, to ease reading
    https://docs.djangoproject.com/en/5.0/ref/django-admin/#dumpdata
    """

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no("This will erase current fixtures files, and will create new ones from exising database."):
            for model in get_models():
                full_path = get_full_path(model)
                try:
                    call_command(
                        "dumpdata", get_model_path(model), "--format", "yaml", "--output", full_path, "--verbosity", 0
                    )
                except CommandError:
                    self.stderr.write(self.style.ERROR(f"⨉ {full_path}"))
                else:
                    # use custom output as dumpdata one is useless
                    self.stdout.write(self.style.SUCCESS(f"✓ {full_path}"))
