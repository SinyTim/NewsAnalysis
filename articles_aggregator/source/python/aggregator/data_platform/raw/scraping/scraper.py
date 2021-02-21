import requests
from bs4 import BeautifulSoup
from pyspark.sql.functions import col
from pyspark.sql.functions import current_timestamp
from pyspark.sql.functions import lit
from pyspark.sql.functions import udf


class Scraper:
    def __init__(self, spark, database, process_name: str, path_source, path_target):

        self.spark = spark
        self.database = database

        self.process_name = process_name

        self.path_source = path_source
        self.path_target = path_target

        self.default_start_state = '1677-09-21 00:12:43.145225'

    def run(self):

        start_state = self.get_last_state()
        audit_id = self.start_audit(start_state)

        df, stop_state = self.extract(start_state)
        df = self.transform(df)
        self.load(df)

        self.stop_audit(audit_id, stop_state)

    def extract(self, time_updated_start):

        df_urls = self.spark.read \
            .format('delta') \
            .load(str(self.path_source)) \
            .filter(col('_time_updated') > lit(time_updated_start))

        time_updated_stop = df_urls \
            .agg({'_time_updated': 'max'}) \
            .collect()[0][0]
        time_updated_stop = time_updated_stop or time_updated_start

        return df_urls, time_updated_stop

    def transform(self, df_urls):

        get_html = udf(self.get_html)
        get_body = udf(self.get_body)

        # todo set number of executors instead of repartition
        df_html = df_urls \
            .repartition(2) \
            .withColumn('html', get_html('url')) \
            .withColumn('html', get_body('html')) \
            .select(col('id').alias('url_id'), 'html')

        return df_html

    def load(self, df_html):
        df_html \
            .withColumn('_time_updated', current_timestamp()) \
            .coalesce(1) \
            .write \
            .format('delta') \
            .mode('append') \
            .save(str(self.path_target))

    @staticmethod
    def get_html(url: str):
        response = requests.get(url)
        html = response.text
        return html

    @staticmethod
    def get_body(page: str):
        soup = BeautifulSoup(page, 'html.parser')
        body = str(soup.body)
        return body

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

    def state_from_str(self, state):
        return state

    def state_to_str(self, state):
        return state
