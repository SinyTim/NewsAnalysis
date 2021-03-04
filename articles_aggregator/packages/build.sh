
conda activate base
conda remove --name pyspark_conda_env --all
conda env create --file environment.yml
conda activate pyspark_conda_env
conda pack --force --output pyspark_conda_env.tar.gz
conda activate base

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir '../../packages'
rm -r build dist articles_aggregator.egg-info
