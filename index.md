# CarthageAPI-1.0
#### Python/Flask REST API endpoints for AWS S3 Bucket 


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

- **Install and configure _AWS CLI_ with an _IAM User_ privileged to create, read, update, delete the _AWS S3 Buckets_**

- **Install and configure _Git_ and _GitBash_**

- **Install and configure _Docker_ and _DockerHub_**

- **Install and configure the _Jenkins_**

- **Install and configure the _Heroku CLI_ for deployment**


## Spin up the whole stack via _Jenkins_

#### The Jenkins pipeline mainly goes through these stages in Series: 

##### Declarative: Checkout SCM
Jenkins obtains a Jenkinsfile in the Git repository.

##### Build
Jenkins clones the Git repository & builds the flask app to run.

##### Test
Jenkins starts testing the REST API Endpoints are active with the CURL commands written in the test-script.sh.

##### Dockerize
Jenkins dockerizes the flask app and pushes the container on DockerHub.

##### Deployment
Jenkins pulls the Docker image to deploy and release the Flask app on Heroku.


#### Follow the instructions in the below visuals to setup Jenkins pipeline job

![image](https://drive.google.com/uc?export=view&id=17_QTdZ-zSHCBCe2zh6EYA_gFDtn_MykX)

![image](https://drive.google.com/uc?export=view&id=1XgNty-K12Im2Y7EHW14sypUpmgsJSn-L)

![image](https://drive.google.com/uc?export=view&id=1vZZ-XlQaSbonViuMu4lB5xUnXxEk3VxY)

![image](https://drive.google.com/uc?export=view&id=191RwT7QO0EoO-AdpvYrbgrmPsXfIvg4n)

![image](https://drive.google.com/uc?export=view&id=1Azr__mYl3gKIJ1SQDJp0bK0Kz4iIMzYB)


> P.S. Kindly write here for more queries and suggestions @**jai.jgec@gmail.com**

> **©** **2020** The Project is publicly intended for learning purpose.
