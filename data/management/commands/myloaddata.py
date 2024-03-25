import warnings

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import transaction

from data.utils.shell_utils import yes_or_no
from .utils import get_models, get_full_path


class Command(BaseCommand):
    help = """Slight wrapper around loaddata to:
    - flush the database first
    - have default parameters
    - have a confirmation prompt
    - remove warnings if a file has no model in it
    """

    @transaction.atomic()
    def handle(self, *args, **options):
        if yes_or_no("This will flush current database and will recreate entries from existing fixtures."):
            call_command("flush", "--noinput")
            self.stdout.write("Exising database has been flushed.")
            for model in get_models():
                # if a model is detected but has no related file, it will raise an error
                full_path = get_full_path(model)
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=RuntimeWarning)
                    call_command(
                        "loaddata",
                        full_path,
                        "--verbosity",
                        2,
                    )
                    self.stdout.write("\n\n")
