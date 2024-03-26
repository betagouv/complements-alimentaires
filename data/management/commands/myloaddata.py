import warnings

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings

from data.utils.shell_utils import yes_or_no
from data.utils.model_utils import get_models


class Command(BaseCommand):
    help = """Slight wrapper around original loaddata command to:
    - flush the database first
    - have default parameters
    - have a confirmation prompt for added safety
    - remove warnings if a file has no model in it
    # https://docs.djangoproject.com/en/5.0/ref/django-admin/#django-admin-loaddata
    """

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no("This will flush current database and will recreate entries from existing fixtures."):
            call_command("flush", "--noinput")
            self.stdout.write("Exising database has been flushed.")
            for model in get_models(settings.FIXTURE_MODELS):
                # if a model is defined but has no related file, it will raise an error
                full_path = settings.FIXTURE_FOLDER / f"{model._meta.app_label}.{model._meta.object_name}.yaml"
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=RuntimeWarning)
                    call_command("loaddata", full_path, "--verbosity", 2)
                    self.stdout.write("\n\n")
