from django.core.management.base import BaseCommand
from search_food.database_fill import create_user


class Command(BaseCommand):
    help = 'Pre fill the database for travis tests'

    def handle(self, *args, **options):
        self.stdout.write('Filling the database...')
        try:
            create_user(
                'testuser61700',
                'testuser@testuser.fr',
                'dedansletest61')
            self.stdout.write('Database filled.')
        except TypeError:
            self.stdout.write('There was a problem during the process')
