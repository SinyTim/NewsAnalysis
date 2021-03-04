
REM pip install --requirement requirements_job.txt --target ./dependencies --upgrade
REM cd dependencies
REM zip -r ../dependencies.zip .
REM cd ..
REM rm -r dependencies

conda remove --name pyspark_conda_env --all
conda create -y -n pyspark_conda_env -c conda-forge conda-pack beautifulsoup4 psycopg2
conda activate pyspark_conda_env
conda pack -f -o pyspark_conda_env.tar.gz

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir "../../packages"
rmdir /s /q build dist articles_aggregator.egg-info
