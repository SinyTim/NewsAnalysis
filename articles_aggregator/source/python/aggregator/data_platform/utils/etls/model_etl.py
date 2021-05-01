from aggregator.data_platform.utils import function


class ModelEtl:

    def __init__(self, path_source, path_model, spark):

        self.path_source = path_source
        self.path_model = path_model

        self.spark = spark

    def run(self):
        df = self.extract()
        model = self.transform(df)
        self.load(model)

    def extract(self):
        return function.read_delta(self.spark, self.path_source)

    def transform(self, df):
        raise NotImplementedError

    def load(self, model):
        raise NotImplementedError
