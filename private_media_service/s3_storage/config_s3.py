import boto3
from moto import mock_aws
from private_media_service.config.config import MODE, LOGIN_S3, PASSWORD_S3, HOST_S3

if MODE == "TEST":
    mock = mock_aws()
    mock.start()
    s3_client = boto3.client('s3', region_name='us-east-1')
    s3_client.create_bucket(Bucket='memes')
else:
    s3_client = boto3.client(
        's3',
        endpoint_url=HOST_S3,
        aws_access_key_id=LOGIN_S3,
        aws_secret_access_key=PASSWORD_S3,
        region_name='us-east-1'
    )
