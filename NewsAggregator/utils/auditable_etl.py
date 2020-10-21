import psycopg2


class AuditableEtl:

    def __init__(self):

        auditdb_url = '127.0.0.1'
        auditdb_name = 'auditdb'
        user_name = 'postgres'
        user_password = 'postgres'

        self.connection = psycopg2.connect(
            host=auditdb_url, database=auditdb_name,
            user=user_name, password=user_password
        )
        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def __del__(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()

    def run(self):

        source = self.get_unprocessed_source()

        if not source:
            return

        destination = self.get_destination()
        audit_ids = self.start_audit(source, destination)

        data = self.extract(source)
        data = self.transform(data)
        self.load(data, destination)

        self.stop_audit(audit_ids)

    def extract(self, source):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data, destination):
        raise NotImplementedError

    def start_audit(self, source, destination):
        raise NotImplementedError

    def stop_audit(self, audit_ids):
        raise NotImplementedError

    def get_unprocessed_source(self):
        raise NotImplementedError

    def get_destination(self):
        raise NotImplementedError
