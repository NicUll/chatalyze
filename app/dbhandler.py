class Column:

    def __init__(self, name, data_type, properties=None):
        self.name = name
        self.data_type = data_type
        self.properties = properties

    def __repr__(self):
        return "%s %s %s" % (self.name, self.data_type, self.properties)


class DBHandler:
    """
    Module for storing and getting db-values to add some abstraction
    from the database and open up for a change of db-type
    """

    def __init__(self):
        pass

    def connect(self, database: str):
        pass

    def close_connection(self):
        pass

    def create_table(self, name: str, columns: list[Column]):
        pass

    def _attach_database(self, database: str, name: str):
        pass

    def _detach_database(self, name: str):
        pass

    def add_temp_db(self, name: str):
        pass

    def remove_temp_db(self, name: str):
        pass
