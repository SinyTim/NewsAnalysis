import sys

from pyspark.sql import SparkSession

import aggregator


# todo
if __name__ == '__main__':
    job_class_str = sys.argv[1]

    spark = SparkSession.builder.getOrCreate()

    params = {'spark': spark}

    eval(job_class_str)(**params).run()
