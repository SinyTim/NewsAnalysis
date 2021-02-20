import psycopg2


class PostgresConnection:

    def __init__(self, config):

        self.host = config['host']
        self.port = config['port']
        self.db_name = config['db_name']
        self.user_name = config['user_name']
        self.user_password = config['user_password']

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
