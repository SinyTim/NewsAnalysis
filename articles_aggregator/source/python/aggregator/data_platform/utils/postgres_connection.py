import psycopg2


class PostgresConnection:

    def __init__(self, host, port, db_name, user_name, user_password):

        self.host = host
        self.port = port
        self.db_name = db_name
        self.user_name = user_name
        self.user_password = user_password

        self.connection = psycopg2.connect(
            host=self.host, port=self.port, database=self.db_name,
            user=self.user_name, password=self.user_password,
        )

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def execute(self, query):
        self.cursor.execute(query)

    def execute_fetchone(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
