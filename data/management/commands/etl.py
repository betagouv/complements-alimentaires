from django.core.management.base import BaseCommand

from config.tasks import export_datasets_to_data_gouv


class Command(BaseCommand):
    help = "Export datasets by synchronously triggering the Celery task"

    def handle(self, *args, **options):
        export_datasets_to_data_gouv(publish=False)
