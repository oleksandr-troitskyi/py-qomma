import csv
from qomma.Domain.Table import Table


class CSVReader:
    def read(self, full_path: str, table_name: str) -> Table:
        file_to_read = open(full_path, encoding='utf-8')
        csv_data = csv.reader(file_to_read)
        data_lines = list(csv_data)

        return Table(table_name.lower(), data_lines)
