

class Etl:

    def run(self):
        data = self.extract()
        data = self.transform(data)
        self.load(data)

    def extract(self):
        raise NotImplementedError

    def transform(self, data):
        raise NotImplementedError

    def load(self, data):
        raise NotImplementedError
