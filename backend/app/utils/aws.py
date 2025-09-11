import os
import boto3
from app.core.config import settings


def get_s3_client():
    endpoint = os.getenv("S3_ENDPOINT_URL")  # http://minio:9000 בלוקאל
    ak = os.getenv("S3_ACCESS_KEY")
    sk = os.getenv("S3_SECRET_KEY")
    params = dict(region_name=settings.AWS_REGION)
    if endpoint:
        params["endpoint_url"] = endpoint
    if ak and sk:
        params["aws_access_key_id"] = ak
        params["aws_secret_access_key"] = sk
    return boto3.client("s3", **params)

