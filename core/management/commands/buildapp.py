import json
import os
import subprocess
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from agregator_ofd.settings.settings import PROJECT_DIR
from core.models import CustomUser

AVAILABLE_BUILD_PARAMETERS = ["test", "development", "production"]


class Command(BaseCommand):
    """
    Building parametrized script:
    Takes as --profile parameter one of AVAILABLE_BUILD_PARAMETERS.
    Each parameter name require file in agregator_ofd/settings/parameter_file.py with import * from common file.

    Example: $ python manage.py buildapp --profile development
    """

    help = 'Builds an app based on given parameter, example: --profile production'

    def add_arguments(self, parser):
        parser.add_argument(
            '--profile',
            dest='profile',
            required=True,
            help=f'Select building profile: {AVAILABLE_BUILD_PARAMETERS}',
        )

    def handle(self, *args, **options):
        """
        Running every build command and print status to user.

        :param args: None
        :param options: profile name as string
        :return: None
        """
        # Running pytest for all project's app
        profile = options['profile']

        if profile not in AVAILABLE_BUILD_PARAMETERS:
            self.stdout.write(self.style.ERROR('Invalid profile parameter. Theese are available parameters:'))
            for available_profile in AVAILABLE_BUILD_PARAMETERS:
                self.stdout.write(available_profile + ",\n")
            exit()

        # set environment variable
        self.__load_environment_variables()

        # Check if settings are correct (are equal to building profile ex. test=test)
        with open(os.path.join(PROJECT_DIR, 'agregator_ofd/settings/settings.py'), 'r+') as settings_file:
            settings_file_content = settings_file.read()

        # When profile mismatch change settings and terminate script with message to rerun script
        if profile + " " not in settings_file_content:
            with open(os.path.join(PROJECT_DIR, 'agregator_ofd/settings/settings.py'), 'w') as settings_file:
                settings_file.write('from .%s import *' % profile)
                settings_file.truncate()
                # Inform user about changed configuration
                self.stdout.write(self.style.ERROR('Replaced database configuration, rerun script.'))
                exit(1)

        # when env is PRODUCTION, pass DB removal
        print("DB: " + settings.DATABASES['default']['NAME'])
        if not self.__is_production_environment(profile):
            print("This stage is not build under production")
            # When database is sqlite so we need to remove a file (db)
            if "sqlite" in settings.DATABASES['default']['NAME']:
                if os.path.exists(os.path.join(PROJECT_DIR, 'db.sqlite3')):
                    os.remove(os.path.join(PROJECT_DIR, 'db.sqlite3'))
            # When database is connected normally run cleardatabase command
            else:
                call_command('cleardatabase')
                call_command('removemigrations')
        # when env is any kind, call upgrade/update commands
        # collect static files - standard django command
        call_command('collectstatic', interactive=False)

        # make new migration files - standard django command
        call_command('makemigrations', interactive=False)

        #  populate db based on migration files
        call_command('migrate', interactive=False)

        # when env is PRODUCTION, pass DB seeding
        if not self.__is_production_environment(profile):
            self.stdout.write(self.style.SUCCESS('Creating default superuser.'))
            CustomUser.objects.create_superuser("admin", "admin@admin.pl", "admin")
            self.stdout.write(self.style.SUCCESS('Created user account: l: admin, pw: admin'))
            call_command('initializedata')

        #  run all tests created with py_test lib
        call_command('pytest_runner')

        # print information about finish of building process
        self.stdout.write(self.style.SUCCESS('>>>>>>>>>>>>>>>>>>>>>>>>> Successful build <<<<<<<<<<<<<<<<<<<<<<<<<<'))

    def __load_environment_variables(self):
        """
        Protected method, to load environment vars
        form app_settings.json file while building solution
        :return: void
        """
        self.stdout.write(self.style.SUCCESS(
            '>>>>>>>>>>>>>>>>>>>>>>>>> Start adding environment variables <<<<<<<<<<<<<<<<<<<<<<<<<<'))
        with open('app_settings.json') as json_environemnt_vars:
            environment_vars = json.load(json_environemnt_vars)
            for key, value in environment_vars.items():
                os.environ[key] = str(value)
                self.stdout.write(self.style.SUCCESS(
                    f"{key}:{value}"))

        self.stdout.write(self.style.SUCCESS(
            '>>>>>>>>>>>>>>>>>>>>>>>>> Finished adding environment variables <<<<<<<<<<<<<<<<<<<<<<<<<<'))

    def __is_production_environment(self, profile: str):
        """
        Protected method responsible for checking, does project suppose
        to be created with production environment
        :param profile:
        :return:
        """
        is_prod_env_var = os.environ.get('PRODUCTION', "False")
        is_prod_env = True if is_prod_env_var == "True" else False
        if is_prod_env and profile == "production":
            self.stdout.write(
                self.style.WARNING(
                    '>>>>>>>>>>>>>>>>>>>>>>>>> Building with production environment! <<<<<<<<<<<<<<<<<<<<<<<<<<'))
            return True
        if is_prod_env and profile != "production":
            self.stdout.write(
                self.style.WARNING(
                    f'>>>>>>>>>>>>>>>>>>>>>>>>> You set production env, but profile is {profile}. <<<<<<<<<<<<<<<<<<<<<<<<<<'))
        if not is_prod_env and profile == "production":
            self.stdout.write(
                self.style.WARNING(
                    f'>>>>>>>>>>>>>>>>>>>>>>>>> You did not set env, but profile is {profile}. <<<<<<<<<<<<<<<<<<<<<<<<<<'))
        return False
