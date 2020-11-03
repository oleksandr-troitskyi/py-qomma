import unittest
from unittest.mock import MagicMock
from qomma.Domain.Query import Query
from qomma.Domain.Table import Table


class TestTable(unittest.TestCase):
    def test_table_returns_correct_values(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        self.assertEqual(table.get_name(), 'table_name')
        self.assertEqual(table.get_column_names(),
                         ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'])
        self.assertEqual(table.get_rows(), [['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
                                            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
                                            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
                                            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])

    def test_table_selects_simple_query_with_one_field(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        query = Query()
        query.get_select_expression = MagicMock(return_value=['id'])
        query.get_aggregate_function = MagicMock(return_value='')
        query.get_where_clause = MagicMock(return_value=[])

        self.assertEqual(table.select_rows(query), [['1'], ['2'], ['3'], ['4']])

    def test_table_selects_simple_query_from_task(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        query = Query()
        query.get_select_expression = MagicMock(return_value=['company', 'country'])
        query.get_aggregate_function = MagicMock(return_value='')
        query.get_where_clause = MagicMock(return_value=[])

        self.assertEqual(table.select_rows(query),
                         [['id Software', 'USA'], ['id Software', 'USA'], ['Tesla', 'USA'], ['Williams', 'UK']])

    def test_table_selects_with_simple_where_clause(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        query = Query()
        query.get_select_expression = MagicMock(return_value=['first_name', 'last_name'])
        query.get_aggregate_function = MagicMock(return_value='')
        query.get_where_clause = MagicMock(return_value=[('', 'country', 'USA')])

        self.assertEqual(table.select_rows(query),
                         [['John', 'Carmack'], ['Jonn', 'Romero'], ['Elon', 'Musk']])

    def test_table_selects_with_coplicated_where_clause(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        query = Query()
        query.get_select_expression = MagicMock(return_value=['first_name', 'last_name'])
        query.get_aggregate_function = MagicMock(return_value='')
        query.get_where_clause = MagicMock(return_value=[('', 'country', 'USA'), ('AND', 'company', 'id Software')])

        self.assertEqual(table.select_rows(query),
                         [['John', 'Carmack'], ['Jonn', 'Romero']])

    def test_table_selects_with_count_expression(self):
        table = Table('table_name', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']
        ])
        query = Query()
        query.get_select_expression = MagicMock(return_value=[])
        query.get_aggregate_function = MagicMock(return_value='COUNT(*)')
        query.get_where_clause = MagicMock(return_value=[('', 'country', 'USA')])

        self.assertEqual(table.select_rows(query),
                         [3])
