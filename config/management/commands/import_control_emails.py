from django.core.management.base import BaseCommand

from config.tasks import import_control_emails


class Command(BaseCommand):
    help = "Import email addresses for control roles by synchronously triggering the Celery task"

    def handle(self, *args, **options):
        import_control_emails()
