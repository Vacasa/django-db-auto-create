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
            if re.search(r'FATAL:  database "\S+?" does not exist', str(exception)):
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

        if database_vendor == "postgresql":
            database_config = settings.DATABASES[database]
            postgres_database_config = deepcopy(database_config)
            postgres_database_config["NAME"] = "postgres"
            handler = ConnectionHandler(
                databases={DEFAULT_DB_ALIAS: postgres_database_config}
            )

            database_name = database_config["NAME"]
            with handler[DEFAULT_DB_ALIAS].cursor() as cursor:
                cursor.execute("CREATE DATABASE \"{}\"".format(database_name))

            self.stdout.write("Auto-created database '{}'".format(database_name))
            return True

        return False
