from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    """
    Clears database in current settings profile environment: production, development etc.

    Example: $ python manage.py cleardatabase
    """

    help = 'Clears current settings environment database'

    def handle(self, *args, **options):
        """
        Connect to current db, make query and drops each table, inform if any table can not be dropped.

        :param args: None
        :param options: None
        :return: None
        """

        cursor = connection.cursor()
        cursor.execute(
            """SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type != 'VIEW' AND table_name NOT LIKE 'pg_ts_%%'""")
        rows = cursor.fetchall()
        for row in rows:
            try:
                cursor.execute('drop table %s cascade ' % row[0])
            except:
                self.stdout.write(self.style.SUCCESS("could not drop %s" % row[0]))
        self.stdout.write(
            self.style.SUCCESS('>>>>>>>>>>>>>>>>>>>>>>>>> Successful database dropped <<<<<<<<<<<<<<<<<<<<<<<<<<'))
