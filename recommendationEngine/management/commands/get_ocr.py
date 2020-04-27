from django.core.management.base import BaseCommand, CommandError
from recommendationEngine.Utils.OCRimage import ocr_extract_from_images



class Command(BaseCommand):
    help = 'create image data from ocr and push to db'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        ocr_extract_from_images()