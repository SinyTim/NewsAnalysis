import psycopg2


class UrlGenerator:

    def __init__(self, source: str, process_name: str, url_template: str, default_start_state: str):

        auditdb_url = '127.0.0.1'
        auditdb_name = 'auditdb'
        user_name = 'postgres'
        user_password = 'postgres'

        self.source = source
        self.process_name = process_name
        self.url_template = url_template
        self.default_start_state = default_start_state

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
        start_state = self._get_last_state()

        generation_id = self._start(start_state)

        urls, urls_bad, stop_state = self._generate(start_state)

        if len(urls) != 0:
            self._write_urls(urls, generation_id)

        if len(urls_bad) != 0:
            self._write_bad_urls(urls_bad, generation_id)

        self._stop(generation_id, stop_state, len(urls))

    def _generate(self, start_state):
        raise NotImplementedError

    def _state_from_str(self, state: str):
        raise NotImplementedError

    def _state_to_str(self, state):
        raise NotImplementedError

    def _get_urls_from_state(self, state):
        raise NotImplementedError

    def _increment_state(self, state):
        raise NotImplementedError

    def _get_last_state(self):
        query = f"select get_generation_last_state('{self.source}');"
        self.cursor.execute(query)
        state = self.cursor.fetchone()[0] or self.default_start_state
        state = self._state_from_str(state)
        return state

    def _start(self, start_state):
        start_state = self._state_to_str(start_state)
        query = f"select start_url_generation('{self.source}', '{start_state}', '{self.process_name}');"
        self.cursor.execute(query)
        generation_id = self.cursor.fetchone()[0]
        return generation_id

    def _stop(self, generation_id: int, stop_state, n_urls: int):
        stop_state = self._state_to_str(stop_state)
        query = f"select stop_url_generation({generation_id}, '{stop_state}', {n_urls});"
        self.cursor.execute(query)

    def _write_urls(self, urls, generation_id: int):
        values = urls.map(lambda url: f"('{url}',{generation_id})")
        values = ','.join(values)
        query = f'insert into urls (url, url_generation_id) values {values} on conflict (url) do nothing;'
        self.cursor.execute(query)

    def _write_bad_urls(self, bad_urls, generation_id: int):
        values = bad_urls.apply(
            lambda row: f"('{row['url']}',{generation_id},{row['status_code']},'{row['url_response']}')",
            axis=1
        )
        values = ','.join(values)
        query = f'insert into bad_urls (url, url_generation_id, status_code, url_response) values {values};'
        self.cursor.execute(query)
