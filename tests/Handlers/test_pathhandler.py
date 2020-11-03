import unittest
from unittest.mock import MagicMock
from qomma.Readers.ReaderFactory import ReaderFactory
from qomma.Handlers.PathHandler import PathHandler
import os


class TestPathHandler(unittest.TestCase):
    def test_it_handles_unexisted_path(self):
        reader_factory = ReaderFactory()
        path_handler = PathHandler(reader_factory)
        result = path_handler.handle('asdfasf')
        self.assertEqual(result.get_error(), 'Path incorrect')
        self.assertEqual(result.get_name(), '')
        self.assertEqual(result.get_tables(), {})

    def test_it_handles_empty_folder(self):
        path = './fake_dir'
        os.mkdir(path)
        reader_factory = ReaderFactory()
        path_handler = PathHandler(reader_factory)
        result = path_handler.handle(path)
        self.assertEqual(result.get_error(), '')
        self.assertEqual(result.get_name(), 'fake_dir')
        self.assertEqual(result.get_tables(), {})
        os.rmdir(path)

    def test_it_handles_folder_with_csv(self):
        path = './csvs'
        reader_factory = ReaderFactory()
        reader_factory.create = MagicMock()
        path_handler = PathHandler(reader_factory)
        result = path_handler.handle(path)
        self.assertEqual(result.get_error(), '')
        self.assertEqual(result.get_name(), 'csvs')
        reader_factory.create.assert_called_once_with(['drivers', 'csv'])
