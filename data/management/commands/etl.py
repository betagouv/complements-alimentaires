from django.core.management.base import BaseCommand

from config.tasks import export_datasets_to_data_gouv


class Command(BaseCommand):
    help = "Export datasets by synchronously triggering the Celery task"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("batch_size", type=int)

    def handle(self, *args, **options):
        self.stdout.write("Starting datasets export...")
        export_datasets_to_data_gouv(publish=False, batch_size=options["batch_size"])

        self.stdout.write(self.style.SUCCESS("Datasets export completed!"))
