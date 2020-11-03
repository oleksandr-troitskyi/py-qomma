from qomma.Domain.Query import Query


class Table:
    def __init__(self, name: str, items: list):
        self.__name = name
        self.__columns = []
        self.__rows = []
        if len(items) > 0:
            columns_raw = items.pop(0)
            for column in columns_raw:
                self.__columns.append(column.replace(' ', ''))
            for row in items:
                line = []
                for cell in row:
                    line.append(cell.strip())
                self.__rows.append(line)

    def get_name(self) -> str:
        return self.__name

    def get_column_names(self) -> list:
        return self.__columns

    def get_rows(self) -> list:
        return self.__rows

    def select_rows(self, query: Query) -> list:
        selected = []

        keys = self.__get_keys(query.get_select_expression())

        for row in self.__rows:
            formed_row = []

            if self.__is_satisfied_by_where_clause(row, query.get_where_clause()):
                if query.get_aggregate_function() != '':
                    if query.get_aggregate_function() == 'COUNT(*)':
                        formed_row = row
                else:
                    for key in keys:
                        formed_row.append(row[key])

                selected.append(formed_row)

        if query.get_aggregate_function() != '':
            return [len(selected)]

        return selected

    def __get_keys(self, fields: list) -> list:
        keys = []
        for field in fields:
            keys.append(self.__columns.index(field))

        return keys

    def __is_satisfied_by_where_clause(self, row: list, where_clause: list) -> bool:
        satisfied = True

        for i in range(len(where_clause)):
            sat = False
            key = self.__columns.index(where_clause[i][1])
            if row[key].strip() == where_clause[i][2]:
                sat = True
            if where_clause[i][0] == '':
                satisfied = sat
            elif where_clause[i][0] == 'AND' and satisfied == True and sat == True:
                satisfied = True
            elif where_clause[i][0] == 'OR' and (satisfied == True or sat == True):
                satisfied = True
            else:
                satisfied = False

        return satisfied
