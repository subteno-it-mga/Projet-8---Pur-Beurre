from django.core.management.base import BaseCommand
from search_food.translation import translate_po
import os


class Command(BaseCommand):
    help = 'Translation program'
    def add_arguments(self, parser):
        parser.add_argument('language_to', type=str)

    def handle(self, *args, **options):
        self.stdout.write('Try translate')
        language_to = options['language_to']
        try:
            translate_po(language_to)
        except TypeError:
            self.stdout.write('There was a problem during the process')
