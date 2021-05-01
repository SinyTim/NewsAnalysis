from abc import ABC

from aggregator.data_platform.utils.postgres_connection import PostgresConnection


class IncrementalEtl(ABC):

    def __init__(self,
                 database: PostgresConnection,
                 process_name: str,
                 default_start_state: str):

        self.database = database
        self.process_name = process_name
        self.default_start_state = default_start_state

    def run(self):

        start_state = self.get_last_state()
        audit_id = self.start_audit(start_state)

        df, stop_state = self.extract(start_state)
        df = self.transform(df)
        self.load(df)

        self.stop_audit(audit_id, stop_state)

    def extract(self, start_state):
        raise NotImplementedError

    def transform(self, df):
        raise NotImplementedError

    def load(self, df):
        raise NotImplementedError

    def get_last_state(self):
        query = f"select get_audit_last_state('{self.process_name}');"
        state = self.database.execute_fetchone(query)[0]
        state = state or self.default_start_state
        state = self.state_from_str(state)
        return state

    def start_audit(self, start_state):
        start_state = self.state_to_str(start_state)
        query = f"select start_audit('{self.process_name}', '{start_state}');"
        audit_id = self.database.execute_fetchone(query)[0]
        return audit_id

    def stop_audit(self, audit_id: int, stop_state):
        assert stop_state
        stop_state = self.state_to_str(stop_state)
        query = f"select stop_audit({audit_id}, '{stop_state}');"
        self.database.execute(query)

    def state_from_str(self, state: str):
        return state

    def state_to_str(self, state) -> str:
        return state
