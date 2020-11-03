from qomma.Readers.CSVReader import CSVReader


class ReaderFactory:
    def create(self, table_parts: list) -> CSVReader:
        if table_parts[1] == 'csv':
            return CSVReader()

        raise Exception("This type of file is not supported at this moment")
