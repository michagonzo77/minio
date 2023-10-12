from minio import Minio
from pyminioadmin import MinioAdminClient
from .secrets_minio import get_minio_secrets

def getclient():
    miniohost, minioaccesskey, miniosecretkey = get_minio_secrets()
    client = Minio(miniohost, minioaccesskey, miniosecretkey, secure=False, cert_check=False)
    return client

def getadminclient():
    miniohost, minioaccesskey, miniosecretkey = get_minio_secrets()
    client = MinioAdminClient(miniohost, minioaccesskey, miniosecretkey, secure=False, cert_check=False)
    return client