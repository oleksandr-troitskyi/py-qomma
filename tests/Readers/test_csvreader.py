import unittest
from qomma.Domain.Table import Table
from qomma.Readers.CSVReader import CSVReader


class TestReaderFactory(unittest.TestCase):
    def test_it_returns_table(self):
        reader = CSVReader()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])

        self.assertIsInstance(reader.read('./csvs/drivers.csv', 'drivers'), Table)
        self.assertEqual('drivers', table.get_name())
        self.assertEqual(['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
                         table.get_column_names())
        self.assertEqual([['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
                          ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
                          ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
                          ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']], table.get_rows())
