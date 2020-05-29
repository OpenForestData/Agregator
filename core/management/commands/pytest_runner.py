import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Run all tests with pytest lib
    Example: $ python manage.py pytest_runner, but simpler is pytest in cmdln.
    """

    help = 'Running all project tests with pytest lib'

    def handle(self, *args, **options):
        """
        Running all tests with pytests as subprocess,
        when there are any failures, or no tests found exit process
        """

        process_finish = subprocess.run('pytest')
        if not process_finish.returncode == 0:
            self.stdout.write(self.style.ERROR('>>>>>>>>>>>>>>>>>>>>>>>>> Tests failed <<<<<<<<<<<<<<<<<<<<<<<<<<'))
            exit()
