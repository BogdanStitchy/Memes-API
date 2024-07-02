import boto3
from botocore.exceptions import ClientError
from moto import mock_aws

from private_media_service.config.config import MODE, LOGIN_S3, PASSWORD_S3, HOST_S3


def create_bucket_if_not_exists(s3_client, bucket_name):
    try:
        s3_client.head_bucket(Bucket=bucket_name)  # проверка существования бакета
    except ClientError:
        s3_client.create_bucket(Bucket=bucket_name)  # бакет не существует, создаем новый бакет


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
    create_bucket_if_not_exists(s3_client, "memes")
