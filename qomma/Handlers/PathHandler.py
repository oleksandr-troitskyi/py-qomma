import os
from qomma.Domain.Database import Database
from qomma.Domain.Query import Query
from qomma.Readers.ReaderFactory import ReaderFactory


class PathHandler:
    """
    Class created to handle the analysis of path that user provided
    """

    def __init__(self, reader_factory: ReaderFactory):
        self.__reader_factory = reader_factory

    def handle(self, path: str) -> Database:
        """
        Method receives path as a string and tries to reach this path.
        If path is incorrect, it returns Database entity with error message.
        In case of succeed, function goes through each file and tries to pass it through a factory, that returns
        reader or fails if no suitable reader found for this specific file.
        :param path: str
        :return: Database
        """

        if not os.path.isdir(path):
            database = Database('', Query())
            database.set_error('Path incorrect')
            return database

        database_name = os.path.basename(os.path.normpath(path))
        database = Database(database_name, Query())

        files = os.listdir(path)
        for file in files:
            table_parts = file.split('.')

            try:
                table = self.__reader_factory.create(table_parts).read(path + '/' + file, table_parts[0])
                database.add_table(table)
            except:
                pass

        return database
