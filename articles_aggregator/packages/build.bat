
cd ../source/python

python setup.py sdist bdist_wheel --dist-dir "../../packages"

rmdir /s /q build dist articles_aggregator.egg-info
