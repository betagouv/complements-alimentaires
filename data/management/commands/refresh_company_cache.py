from django.core.management.base import BaseCommand

from config.tasks import update_market_ready_counts


class Command(BaseCommand):
    help = "Refresh the market-ready declarations count cache for all companies by synchronously triggering the Celery task"

    def handle(self, *args, **options):
        self.stdout.write("Starting cache update...")
        update_market_ready_counts()

        self.stdout.write(self.style.SUCCESS("Synchronous cache refresh completed!"))
