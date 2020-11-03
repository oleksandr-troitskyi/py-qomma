import unittest
from qomma.Readers.ReaderFactory import ReaderFactory
from qomma.Readers.CSVReader import CSVReader


class TestReaderFactory(unittest.TestCase):
    def test_it_returns_csv_reader(self):
        factory = ReaderFactory()
        self.assertIsInstance(factory.create(['drivers', 'csv']), CSVReader)

    def test_it_exposes_exception(self):
        factory = ReaderFactory()
        with self.assertRaises(Exception) as context:
            factory.create(['drivers', 'sfd'])

        self.assertTrue('This type of file is not supported at this moment' in str(context.exception))
