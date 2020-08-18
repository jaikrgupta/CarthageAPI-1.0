# CarthageAPI-1.0
Python/Flask REST API endpoints for AWS S3 Bucket 


## Simple CURL Commands to test the REST API Endpoints

### GET /files - retrieves a list of files from AWS S3 bucket

`curl http://127.0.0.1:5000/files`

### GET /files/:id - retrieves a spicific file

`curl -O http://127.0.0.1:5000/files/file_id`

### POST /files - uploads file into S3 bucket

`curl -F file="@pathto/or/filename" http://127.0.0.1:5000/files`

### DELETE /files/:id - deletes a specific file from S3 bucket

`curl -X DELETE http://127.0.0.1:5000/files/file_id`


## Prerequisites

- **Install and configure _AWS CLI_ with an _IAM User_ with privileges to create, read, update, delete the _AWS S3 Buckets_**

- **Install and configure _Docker_ and _DockerHub_**

- **Install and configure _Git_ and _GitBash_**

- **Install and configure the _Jenkins_**

- **Install and configure the _Heroku CLI_ for deployment**

## Spin up the whole stack via _Jenkins_

![image](https://drive.google.com/uc?export=view&id=17_QTdZ-zSHCBCe2zh6EYA_gFDtn_MykX)

![image](https://drive.google.com/uc?export=view&id=1XgNty-K12Im2Y7EHW14sypUpmgsJSn-L)

![image](https://drive.google.com/uc?export=view&id=1zyL9CdXnCYc128CNSouLpSTD8oIss1Au)

![image](https://drive.google.com/uc?export=view&id=191RwT7QO0EoO-AdpvYrbgrmPsXfIvg4n)


> P.S. Kindly write here for more queries and suggestions @ **jai.jgec@gmail.com**


> **©** The Project is intended for learning purpose.
