class Query:
    def __init__(self):
        self.__select_expression = []
        self.__aggregate_function = ''
        self.__table = ''
        self.__where = []
        self.__result = []

    def set_select_expression(self, select_expression: list) -> None:
        self.__select_expression = select_expression

    def get_select_expression(self) -> list:
        return self.__select_expression

    def set_aggregate_function(self, aggregate_function: str) -> None:
        self.__aggregate_function = aggregate_function

    def get_aggregate_function(self) -> str:
        return self.__aggregate_function

    def set_table(self, table: str):
        self.__table = table

    def get_table(self) -> str:
        return self.__table

    def add_where_clause(self, joint_expression: str, column: str, value: str):
        self.__where.append((joint_expression, column, value))

    def get_where_clause(self) -> list:
        return self.__where

    def set_result(self, result: list):
        self.__result = result

    def get_result(self) -> list:
        return self.__result
