import unittest
from unittest.mock import MagicMock
from qomma.Controllers.Controller import Controller
from qomma.Domain.Database import Database
from qomma.Domain.Query import Query
from qomma.Domain.Table import Table
from io import StringIO
from unittest.mock import patch


class TestController(unittest.TestCase):
    @patch('qomma.Controllers.Controller.input', return_value='\q')
    def test_init(self, input):
        database = Database('db_name', Query())
        controller = Controller()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            controller.init(database)
            self.assertEqual(fake_out.getvalue(), 'Tables found: 0\n')

    @patch('qomma.Controllers.Controller.input', return_value='\q')
    def test_init_with_database(self, input):
        query = Query()
        query.get_aggregate_function = MagicMock(return_value='COUNT(*)')
        query.get_result = MagicMock(return_value=[3])

        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        controller = Controller()

        with patch('sys.stdout', new=StringIO()) as fake_out:
            controller.init(database)
            self.assertEqual(fake_out.getvalue(), 'Tables found: 1\ndrivers\n')
