import os

from django.core.management import BaseCommand

from agregator_ofd.settings.settings import PROJECT_DIR


class Command(BaseCommand):
    """
    Command to remove every module migration files.

    Example $ python manage.py removemigrations
    """

    help = 'Removes each projects app migration files.'

    def handle(self, *args, **options):
        for root, directories, filenames in os.walk(PROJECT_DIR):
            dir_name = os.path.split(os.path.abspath(root))
            if 'venv' in dir_name[0]:
                continue
            if dir_name[1] == "migrations":
                    for file_name in filenames:
                        if file_name == "__init__.py":
                            continue
                        else:
                            self.stdout.write(
                                self.style.SUCCESS('{} Removing migration file: {}.'.format(dir_name[0], file_name)))
                            os.remove(os.path.join(root, file_name))
