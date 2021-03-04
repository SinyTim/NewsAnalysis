
pip install --requirement requirements_job.txt --target ./dependencies --upgrade
cd dependencies
zip -r ../dependencies.zip .
cd ..
rm -r dependencies
REM tar -a -c -f dependencies.zip ./dependencies
REM rmdir /s /q dependencies

cd ../source/python
python setup.py sdist bdist_wheel --dist-dir "../../packages"
rmdir /s /q build dist articles_aggregator.egg-info
