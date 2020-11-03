import unittest
from unittest.mock import MagicMock
from qomma.Domain.Query import Query
from qomma.Domain.Database import Database
from qomma.Domain.Table import Table


class TestQuery(unittest.TestCase):
    def test_database_default(self):
        query = Query()
        database = Database('database_name', query)
        self.assertEqual(database.get_name(), 'database_name')
        self.assertEqual(database.get_tables(), {})
        self.assertEqual(database.get_error(), '')
        self.assertEqual(database.has_error(), False)
        self.assertEqual(database.get_query(), query)

    def test_database_setters(self):
        query = Query()
        query.set_table('tada')
        table = Table('table_name', [])
        error_text = 'some error'
        database = Database('database_name', query)
        database.add_table(table)
        database.set_error(error_text)
        self.assertEqual(database.get_name(), 'database_name')
        self.assertEqual(database.get_tables(), {'table_name': table})
        self.assertEqual(database.get_error(), error_text)
        self.assertEqual(database.has_error(), True)
        self.assertEqual(database.get_query(), query)

    def test_database_proceed_empty_query_string(self):
        query = Query()
        database = Database('database_name', query)
        database.proceed_query('')
        self.assertEqual(database.get_error(), 'Wrong query syntax, please try again')

    def test_database_proceed_filled_query_string_with_table_not_exist(self):
        query = Query()
        database = Database('database_name', query)
        database.add_table(Table('drivers', []))
        database.proceed_query('SELECT company, country FROM drivers1;')
        self.assertEqual(database.get_error(), 'Table not exist')

    def test_database_proceed_filled_query_string_with_table_exist_fills_query_table_field(self):
        query = Query()
        database = Database('database_name', query)
        database.add_table(Table('drivers', []))
        database.proceed_query('SELECT company, country FROM drivers;')
        self.assertEqual(database.get_query().get_table(), 'drivers')

    def test_it_fills_aggregate_function_field(self):
        query = Query()
        query.set_aggregate_function = MagicMock()
        database = Database('database_name', query)
        database.add_table(Table('drivers', []))
        database.proceed_query('SELECT COUNT(*) FROM drivers;')
        query.set_aggregate_function.assert_called_once_with('COUNT(*)')

    def test_it_fills_select_expression(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query('SELECT first_name FROM drivers;')
        self.assertEqual(database.get_query().get_select_expression(), ['first_name'])

    def test_it_fills_select_expression_with_multiple_fields(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query('SELECT first_name, last_name FROM drivers;')
        self.assertEqual(database.get_query().get_select_expression(), ['first_name', 'last_name'])

    def test_it_fills_select_expression_with_star_and_id(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query('SELECT *, id FROM drivers;')
        self.assertEqual(database.get_query().get_select_expression(),
                         ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company', 'id'])

    def test_it_fails_if_field_not_exist(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query('SELECT *, id_name FROM drivers;')
        self.assertEqual(database.get_query().get_select_expression(),
                         [])
        self.assertEqual(database.get_error(), 'Field not exist')

    def test_it_shows_error_if_aggregate_function_witout_if_statement(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query('SELECT COUNT(*) FROM drivers;')
        self.assertEqual(database.get_query().get_select_expression(),
                         [])
        self.assertEqual(database.get_error(), 'Query contains aggregate function, but WHERE statement missed')

    def test_it_parses_simple_where_statement_with_non_existed_field(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name FROM drivers WHERE if1 = 'USA';")
        self.assertEqual(database.get_error(), 'Column from where_expression not found')

    def test_it_parses_simple_where_statement_with_existed_field(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name FROM drivers WHERE country = 'USA';")
        self.assertEqual(database.get_query().get_where_clause(), [('', 'country', 'USA')])

    def test_it_parses_complicated_where_statement_with_second_non_existed_field(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name FROM drivers WHERE country = 'USA' AND df = 'sdf';")
        self.assertEqual(database.get_error(), 'Column from where_expression not found')

    def test_it_parses_complicated_where_statement_with_second_existed_field_with_and_statement(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name FROM drivers WHERE country = 'USA' AND company = 'sdf';")
        self.assertEqual(database.get_query().get_where_clause(), [('', 'country', 'USA'), ('AND', 'company', 'sdf')])

    def test_it_parses_complicated_where_statement_with_second_existed_field_with_and_statement(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name FROM drivers WHERE country = 'USA' OR company = 'sdf';")
        self.assertEqual(database.get_query().get_where_clause(), [('', 'country', 'USA'), ('OR', 'company', 'sdf')])

    def test_it_parses_complicated_where_statement_with_lots_of_spaces(self):
        query = Query()
        table = Table('drivers', [
            ['id', 'first_name', 'last_name', 'country', 'year_of_birth', 'company'],
            ['1', 'John', 'Carmack', 'USA', '1970', 'id Software'],
            ['2', 'Jonn', 'Romero', 'USA', '1967', 'id Software'],
            ['3', 'Elon', 'Musk', 'USA', '1971', 'Tesla'],
            ['4', 'Damon', 'Hill', 'UK', '1960', 'Williams']])
        database = Database('database_name', query)
        database.add_table(table)
        database.proceed_query("SELECT first_name,     country FROM drivers WHERE country = 'USA' OR company = 'sdf';")
        self.assertEqual(database.get_query().get_select_expression(), ['first_name', 'country'])
        self.assertEqual(database.get_query().get_where_clause(), [('', 'country', 'USA'), ('OR', 'company', 'sdf')])
