from django.core.management.base import BaseCommand

from config.tasks import assign_control_roles


class Command(BaseCommand):
    help = "Assign control roles based on email list"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Simulate without making changes",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]

        assign_control_roles(dry_run)
