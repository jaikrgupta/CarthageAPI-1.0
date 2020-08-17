#!/bin/sh

mkdir -p test-reports
rm -f test-reports/test_script.log

echo "### Test-script starting to check REST API endpoints on http://127.0.0.1:5000/ ###" >> test-reports/test_script.log

echo "1.) GET /files - retrieves a list of files from AWS S3 bucket" >> test-reports/test_script.log
curl http://127.0.0.1:5000/files >>  test-reports/test_script.log

echo "Check the timestamp before uploading the file" >> test-reports/test_script.log
pwd >> test-reports/test_script.log
ls -lrt >> test-reports/test_script.log

echo "2.) POST /files - uploads file into S3 bucket" >> test-reports/test_script.log
curl -F file="@requirements.txt" http://127.0.0.1:5000/files >> test-reports/test_script.log

echo "3.) GET /files/:id - retrieves a spicific file" >> test-reports/test_script.log
curl -O http://127.0.0.1:5000/files/requirements.txt >> test-reports/test_script.log

echo "Check the timestamp after downloading the file" >> test-reports/test_script.log
pwd >> test-reports/test_script.log
ls -lrt >> test-reports/test_script.log

echo "4.) DELETE /files/:id - deletes a specific file from S3 bucket" >> test-reports/test_script.log
curl -X DELETE http://127.0.0.1:5000/files/requirements.txt >>  test-reports/test_script.log

echo "### Test-script finished checking REST API endpoints on http://127.0.0.1:5000/ ###" >> test-reports/test_script.log