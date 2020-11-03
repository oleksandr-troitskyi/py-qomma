import unittest
from qomma.Domain.Query import Query


class TestQuery(unittest.TestCase):
    def test_query_default(self):
        query = Query()
        self.assertEqual(query.get_select_expression(), [])
        self.assertEqual(query.get_aggregate_function(), '')
        self.assertEqual(query.get_table(), '')
        self.assertEqual(query.get_where_clause(), [])
        self.assertEqual(query.get_result(), [])

    def test_query_setters(self):
        query = Query()
        query.set_select_expression(['country', 'first_name']),
        query.set_aggregate_function('COUNT(*)'),
        query.set_table('table_name'),
        query.add_where_clause('', 'country', 'USA'),
        query.set_result([3]),

        self.assertEqual(query.get_select_expression(), ['country', 'first_name'])
        self.assertEqual(query.get_aggregate_function(), 'COUNT(*)')
        self.assertEqual(query.get_table(), 'table_name')
        self.assertEqual(query.get_where_clause(), [('', 'country', 'USA')])
        self.assertEqual(query.get_result(), [3])
