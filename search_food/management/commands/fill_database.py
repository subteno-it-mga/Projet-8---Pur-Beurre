from django.core.management.base import BaseCommand
from search_food.database_fill import pre_fill_database, clean_database

class Command(BaseCommand):
    help = 'Pre fill the database'

    def handle(self, *args, **options):
        self.stdout.write('Filling the database...')
        try:
            pre_fill_database()
            self.stdout.write('Database filled.')
            clean_database()
        except:
            self.stdout.write('There was a problem during the process')
