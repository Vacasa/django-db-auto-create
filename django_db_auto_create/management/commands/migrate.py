from django.core.management.commands.migrate import Command as MigrateCommand
from django.db import DEFAULT_DB_ALIAS, ConnectionHandler, OperationalError, connections
from django.conf import settings
from copy import deepcopy
import re
import logging

LOGGER = logging.getLogger(__name__)


class Command(MigrateCommand):
    def handle(self, *args, **options):
        try:
            super().handle(*args, **options)
        except OperationalError as exception:
            # Check for postgres or mysql error message
            if re.search(r'(FATAL:  database "\S+?" does not exist|Unknown database \'\S+?\')', str(exception)):
                selected_database = options["database"]
                database_config = settings.DATABASES[selected_database]

                if database_config.get("AUTO_CREATE") and self.create_db(
                    selected_database
                ):
                    super().handle(*args, **options)
                else:
                    raise
            else:
                raise

    def create_db(self, database):
        database_vendor = connections[database].vendor

        # which database can we always connect to?
        CATALOG_DATABASE_NAME = {
            'postgresql': 'postgres',
            'mysql': 'information_schema',
        }

        if database_vendor in ["postgresql", "mysql"]:
            original_database_config = settings.DATABASES[database]
            autocreate_database_config = deepcopy(original_database_config)
            autocreate_database_config["NAME"] = CATALOG_DATABASE_NAME[database_vendor]
            handler = ConnectionHandler({DEFAULT_DB_ALIAS: autocreate_database_config})
            database_name = original_database_config["NAME"]
            with handler[DEFAULT_DB_ALIAS].cursor() as cursor:
                cursor.execute("CREATE DATABASE {}".format(database_name))

            self.stdout.write("Auto-created database '{}'".format(database_name))
            return True

        return False
