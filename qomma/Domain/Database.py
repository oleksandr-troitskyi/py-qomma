from qomma.Domain.Table import Table
from qomma.Domain.Query import Query
import re


class Database:
    """
    This is an Aggregated Entity of Qomma Domain. It implements the business logic. It handles all relations in Domain
    and all business logic it has.
    """

    def __init__(self, name: str, query: Query):
        self.__tables = {}
        self.__name = name
        self.__error = ''
        self.__query = query

    def get_name(self) -> str:
        return self.__name

    def add_table(self, table: Table) -> None:
        self.__tables[table.get_name()] = table

    def get_tables(self) -> dict:
        return self.__tables

    def set_error(self, error: str) -> None:
        self.__error = error

    def get_error(self) -> str:
        return self.__error

    def has_error(self) -> bool:
        return len(self.__error) > 0

    def get_query(self) -> Query:
        return self.__query

    def proceed_query(self, query_string: str) -> None:
        """
        This method process query, that was provided by user of this application.
        Steps are: parse query (do a first level most important validation), check for table existance,
        handle columns (check if columns used in query are presented in a table), handle WHERE expression (if any) and
        finally select rows from table.
        :param query_string: str
        :return: None
        """

        # Check query string for syntax
        parsed_query = self.__parse_query(query_string)
        if self.has_error():
            return

        # check for table existence
        if parsed_query['table_name'] not in self.__tables.keys():
            self.__error = 'Table not exist'
            return
        else:
            self.__query.set_table(parsed_query['table_name'])

        # parse select_expression
        if parsed_query['select_expression'] == 'COUNT(*)':
            self.__query.set_aggregate_function(parsed_query['select_expression'])
        else:
            self.__handle_columns(parsed_query['select_expression'].split(','))
            if self.has_error():
                return

        # go through WHERE condition
        self.__handle_where_statement(parsed_query)
        if self.has_error():
            return

        self.__query.set_result(self.__tables[self.__query.get_table()].select_rows(self.__query))

    def __parse_query(self, query: str) -> dict:
        """
        Method does a parsing of query through the regular expression and creates a dictionary that can be used in
        future operations.
        :param query: str
        :return: dict
        """

        parsed = {}
        result = re.findall(
            r"SELECT ([\w|,|*|(|)|_| ]*|[COUNT(*)]?) FROM ([\w|_]+)( WHERE ([\w| ]+) = '([\w|,|*|(|)| ]+)'( (AND|OR) ([\w|_]+) = '([\w| ]+)')*)*;",
            query)

        if len(result) == 0:
            self.__error = 'Wrong query syntax, please try again'
            return parsed

        parsed['select_expression'], parsed['table_name'], parsed['where_expression'], parsed['where_column1'], parsed[
            'where_value1'], parsed['where_condition_expression'], parsed['logic_operator'], parsed['where_column2'], \
        parsed['where_value2'] = result[0]
        parsed['select_expression'] = parsed['select_expression'].replace(' ', '')
        parsed['table_name'] = parsed['table_name'].replace(' ', '')

        return parsed

    def __handle_columns(self, fields: list) -> None:
        """
        Method goes through the select_expression and check for it's consistency.

        :param fields: list
        :return: None
        """
        columns = []
        table = self.__tables[self.__query.get_table()]
        for field in fields:
            if field == '':
                self.__error = 'Empty field value'
                return
            elif field == '*':
                for item in table.get_column_names():
                    columns.append(item)
            elif field in table.get_column_names():
                columns.append(field)
            else:
                self.__error = 'Field not exist'
                return

        self.__query.set_select_expression(columns)

    def __handle_where_statement(self, parsed_query: dict) -> None:
        if parsed_query['where_expression'] != '':
            if parsed_query['where_column1'] in self.__tables[self.__query.get_table()].get_column_names():
                self.__query.add_where_clause('', parsed_query['where_column1'], parsed_query['where_value1'])
            else:
                self.__error = 'Column from where_expression not found'
                return

            if parsed_query['logic_operator'] != '':
                if parsed_query['where_column2'] in self.__tables[self.__query.get_table()].get_column_names():
                    self.__query.add_where_clause(parsed_query['logic_operator'], parsed_query['where_column2'],
                                                  parsed_query['where_value2'])
                else:
                    self.__error = 'Column from where_expression not found'

        if self.__query.get_aggregate_function() != '' and parsed_query['where_expression'] == '':
            self.__error = 'Query contains aggregate function, but WHERE statement missed'
