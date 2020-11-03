from qomma.Domain.Database import Database


class Controller:
    """
    Class it aimed to handle user interface - get commands from user and handle them properly.
    Can be used right after handling the path to Database
    """

    def init(self, database: Database) -> None:
        """
        Method receives Database entity as a param and runs interface through __show_interface function.
        __present_interface method supposed to be used only once on first run of this method.

        :param database:
        :return: None
        """
        self.__present_interface(database)

        while True:
            res = self.__show_interface(database)
            if not res:
                break

    def __show_interface(self, database: Database) -> bool:
        """
        Function shows a command line for this app.
        On receiving a command from user, it passes query to Database entity, which tries to proceed it.
        If Database got an Error, function prints this error.
        In other case, it prints a result.
        On \\q command from user, it simply returns False.

        :param database: Database
        :return: bool
        """
        command = input(self.__present_command_line(database.get_name()))

        if command == '\q':
            return False

        database.proceed_query(command)
        if database.has_error():
            print(database.get_error())
            return True

        if database.get_query().get_aggregate_function() != '':
            print(database.get_query().get_result()[0])
        else:
            for row in database.get_query().get_result():
                join_str = ', '
                print(join_str.join(row))

        return True

    def __present_interface(self, database: Database) -> None:
        """
        Auxiliary function, aimed to show a quantity of tables found, and list them.
        :param database: Database
        :return:
        """
        print(f'Tables found: {len(database.get_tables())}')

        keys = database.get_tables().keys()
        for key in keys:
            print(key)

    def __present_command_line(self, database_name: str) -> str:
        """
        Simple wrap for command line presentation.
        :param database_name: str
        :return: str
        """
        return '\n' + database_name + '=# '
