import boto3
import os
import json
import uuid
from logger import LOGGER

with open("aws_S3_endpoint.json", 'r') as s3_endpoint:
    connection = json.load(s3_endpoint)

s3_bucket = connection['S3_Bucket']

s3 = boto3.resource('s3')

def aws_connectivity_test(s3_bucket):
    if s3_bucket is None:
        LOGGER.info(f'S3: {s3_bucket} - No existing bucket reference in AWS Client')
        return False
    bucket = s3.Bucket(s3_bucket)
    if bucket.creation_date:
        LOGGER.info(f"S3: {s3_bucket} - Bucket exists in AWS Client")
        return True
    else:
        LOGGER.info(f"S3: {s3_bucket} - Bucket does not exists in AWS Client")
        return False

def aws_save_bucket(s3_bucket):
    connection['S3_Bucket'] = s3_bucket
    with open("aws_S3_endpoint.json", 'w') as s3_endpoint:
        json.dump(connection, s3_endpoint, indent='\t')
    LOGGER.info(f'S3: {s3_bucket} - Persisted in AWS Client')

def initialize_S3(bucket_name):
    bucket_name = '-'.join([bucket_name, str(uuid.uuid4())])
    location = {'LocationConstraint': connection['endpoint']['AWS_DEFAULT_REGION']}
    response = s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    LOGGER.debug(response)
    bucket_versioning = s3.BucketVersioning(bucket_name)
    bucket_versioning.enable()
    LOGGER.info(f'S3: {bucket_name} - Bucket Versioning Enabled')
    LOGGER.info(f'S3: {bucket_name} - Created successfully')
    return bucket_name

def delete_all_objects(bucket_name):
    res = []
    bucket = s3.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
    if res != []:
        bucket.delete_objects(Delete={'Objects': res})
    LOGGER.warning(f'S3: {bucket_name} - existing Objects deleted successfully')
    return True

def delete_bucket(bucket_name):
    delete_all_objects(bucket_name)
    response = s3.Bucket(bucket_name).delete()
    LOGGER.debug(response)
    LOGGER.warning(f'S3: {bucket_name} - Deleted successfully')
    return True

def upload_to_bucket(filename):
    bucket = s3_bucket
    upload_file = f'{os.getcwd()}/uploads/{filename}'
    response = s3.Object(bucket, filename).upload_file(Filename=upload_file, ExtraArgs={'ACL': 'public-read', 'ServerSideEncryption': 'AES256', 'StorageClass': 'STANDARD_IA'})
    LOGGER.debug(response)
    LOGGER.info(f'S3: {bucket} - File: {filename} - Uploaded successfully')
    return True

def download_from_bucket(filename):
    bucket = s3_bucket
    download_file = f'{os.getcwd()}/downloads/{filename}'
    response = s3.Object(bucket, filename).download_file(Filename=download_file)
    LOGGER.debug(response)
    LOGGER.info(f'S3: {bucket} - File: {filename} - Downloaded successfully')
    return True

def listing_bucket(bucket_name='', filename=''):
    if bucket_name == '':
        bucket_name = s3_bucket
    bucket = s3.Bucket(bucket_name)
    files = []
    for object in bucket.objects.all():
        files.append(object.key)
    if filename == '':
        LOGGER.info(f'S3: {bucket} - Files found: {files}')
        return files
    if filename in files:
        LOGGER.info(f'S3: {bucket} - File found: {filename}')
        return True
    LOGGER.info(f'S3: {bucket} - File not found: {filename}')
    return False

def delete_into_bucket(filename):
    bucket = s3_bucket
    found = listing_bucket(filename=filename)
    if found:
        response = s3.Object(bucket, filename).delete()
        LOGGER.debug(response)
        LOGGER.info(f'S3: {bucket} - File: {filename} - Deleted successfully')
        return True
    return False

if __name__ == '__main__':
    LOGGER.info("AWS Client started")
else:
    LOGGER.info("AWS Client processing")
    try:
        if not aws_connectivity_test(s3_bucket):
            s3_bucket = None
            for bucket in s3.buckets.all():
                delete_bucket(bucket.name)
            LOGGER.warning("AWS Client - existing buckets dropped successfully")
            s3_bucket = initialize_S3("mybucket-jaikr")
    except Exception:
        LOGGER.exception("Exception in AWS Client initialization")
    finally:
        if s3_bucket is None:
            LOGGER.critical("AWS Client - Something unexpected happened")
            exit(-1)
        aws_save_bucket(s3_bucket)