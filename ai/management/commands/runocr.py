from django.core.management.base import BaseCommand

from ai import ProductLabelOCRPipeline


class Command(BaseCommand):
    help = "Test OCR pipeline"

    def add_arguments(self, parser):
        parser.add_argument("url", type=str)

    def handle(self, *args, **options):
        my_model = ProductLabelOCRPipeline()
        urls = [options["url"]]
        my_model.match_to_db(urls)
        my_model.print_debugger()
