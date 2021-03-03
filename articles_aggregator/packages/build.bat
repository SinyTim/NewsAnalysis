
pip install --requirement requirements_job.txt --target ./dependencies --upgrade
tar -a -c -f dependencies.zip ./dependencies
rmdir /s /q dependencies

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir "../../packages"
rmdir /s /q build dist articles_aggregator.egg-info
