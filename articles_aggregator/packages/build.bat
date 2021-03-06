
call conda activate base
call conda env create --file environment.yml
call conda activate pyspark_conda_env
call conda pack --force --output pyspark_conda_env.tar.gz
call conda activate base
call conda remove --name pyspark_conda_env --all --yes

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir "../../packages"
rm -r build dist articles_aggregator.egg-info
