from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Populates project with initial data.

    Example: $ python manage.py initializedata
    """
    help = 'Inserts initial data'

    def handle(self, *args, **options):
        """
        Running each declared function to seed db

        :param args: None
        :param options: None
        :return: None
        """

        self.stdout.write(
            self.style.SUCCESS(
                '>>>>>>>>>>>>>>>>>>>>>>>>> Successfully initialized Data <<<<<<<<<<<<<<<<<<<<<<<<<<'))