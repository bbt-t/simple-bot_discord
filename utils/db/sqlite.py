import sqlite3

from loader import logger




class Database:
    def __init__(self, path_to_database='data/sql_db.db'):
        self.path_to_database = path_to_database

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_database)

    def execute(self, sql: str, parameters: tuple = tuple(), fetchone=False, fetchall=False, commit=False):
        parameters = tuple(parameters)
        connection = self.connection
        connection.set_trace_callback(self.logger)
        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        data = None
        if commit:
            connection.commit()
        if fetchone:
            data = cursor.fetchone()
        if fetchall:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def logger(statement):
        logger.info(f"\n----------\nExecuting statement {statement}\n----------")

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(f"{item} = ?" for item in parameters.keys())
        return sql, parameters.values()

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users
        (user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(128) NOT NULL,
        warnings INTEGER,
        reg_time DATE NOT NULL)
        """
        self.execute(sql, commit=True)

    def add_user(self,
                 user_id: int,
                 name: str,
                 reg_time,
                 warnings: int = None):
        sql = "INSERT INTO Users (user_id, name, reg_time, warnings) VALUES (?, ?, ?, ?)"
        parameters = (user_id, name, reg_time, warnings)
        self.execute(sql, parameters=parameters, commit=True)

    def add_warnings(self, user_id: int, warnings: int = 1):
        if show_warnings := self.select_warning(user_id=user_id)[0]:
            warnings += show_warnings
        sql = "UPDATE Users SET warnings = ? WHERE ?"
        parameters = (warnings, user_id)
        self.execute(sql, parameters=parameters, commit=True)

    def select_warning(self, **kwargs):
        sql = "SELECT warnings FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def select_all_user(self):
        sql = "SELECT * FROM Users"
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM Users;", fetchone=True)

    def delete_all_users(self):
        self.execute("DELETE FROM Users WHERE True")

    def del_table(self):
        self.execute("DROP TABLE Users")
