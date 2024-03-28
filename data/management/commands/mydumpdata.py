from django.core.management import CommandError, call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from data.utils.shell_utils import yes_or_no
from data.utils.model_utils import get_models


class Command(BaseCommand):
    help = """Slight wrapper around orginal dumpdata command to:
    - have default parameters
    - have a confirmation prompt for added safety
    - create 1 file per model, to ease reading
    https://docs.djangoproject.com/en/5.0/ref/django-admin/#dumpdata
    """

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no("This will erase current fixtures files, and will create new ones from exising database."):
            for model in get_models(settings.FIXTURE_MODELS):
                full_path = settings.FIXTURE_FOLDER / f"{model._meta.app_label}.{model._meta.object_name}.yaml"
                try:
                    call_command(
                        "dumpdata",
                        f"{model._meta.app_label}.{model._meta.object_name}",
                        "--format",
                        "yaml",
                        "--output",
                        full_path,
                        "--verbosity",
                        0,
                    )
                except CommandError:
                    self.stderr.write(self.style.ERROR(f"⨉ {full_path}"))
                else:
                    # use custom output as dumpdata one is useless
                    self.stdout.write(self.style.SUCCESS(f"✓ {full_path}"))
