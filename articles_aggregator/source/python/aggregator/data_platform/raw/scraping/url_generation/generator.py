import pandas as pd
from pyspark.sql.functions import current_timestamp

from aggregator.data_platform.utils import function


class UrlGenerator:

    def __init__(self, spark, database,
                 process_name: str,
                 url_template: str, default_start_state: str,
                 path_target, path_bad_data):

        self.spark = spark
        self.database = database

        self.process_name = process_name

        self.url_template = url_template
        self.default_start_state = default_start_state

        self.path_target = path_target
        self.path_bad_data = path_bad_data

    def run(self):

        start_state = self.get_last_state()
        audit_id = self.start_audit(start_state)

        df_urls, df_urls_bad, stop_state = self.generate(start_state)

        df_urls = function.add_id_column(df_urls)

        if not df_urls.empty:
            self.load(df_urls)

        if not df_urls_bad.empty:
            self.load_bad(df_urls_bad)

        self.stop_audit(audit_id, stop_state)

    def generate(self, start_state):
        raise NotImplementedError

    def state_from_str(self, state: str):
        raise NotImplementedError

    def state_to_str(self, state):
        raise NotImplementedError

    def get_url_with_state(self, state):
        raise NotImplementedError

    def increment_state(self, state):
        raise NotImplementedError

    def load(self, df_urls: pd.DataFrame):
        self.spark \
            .createDataFrame(df_urls) \
            .withColumn('_time_updated', current_timestamp()) \
            .coalesce(1) \
            .write \
            .format('delta') \
            .mode('append') \
            .save(str(self.path_target))  # todo merge by url

    def load_bad(self, df_urls_bad: pd.DataFrame):
        self.spark \
            .createDataFrame(df_urls_bad) \
            .coalesce(1) \
            .write \
            .format('delta') \
            .mode('append') \
            .save(str(self.path_bad_data))

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
        stop_state = self.state_to_str(stop_state)
        query = f"select stop_audit({audit_id}, '{stop_state}');"
        self.database.execute(query)
