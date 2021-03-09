
conda activate base
conda remove --name pyspark_conda_env --all
pip uninstall pymystem3 --yes
conda env create --file environment.yml
conda activate pyspark_conda_env
conda pack --force --output pyspark_conda_env.tar.gz
conda activate base
pip install pymystem3

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir '../../packages'
rm -r build dist articles_aggregator.egg-info
