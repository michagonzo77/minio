from .actions import action_store

def get_minio_secrets():
    miniohost = action_store.secrets.get("MINIO_HOST")
    minioaccesskey = action_store.secrets.get("MINIO_ACCESSKEY")
    miniosecretkey = action_store.secrets.get("MINIO_SECRETKEY")
    return miniohost, minioaccesskey, miniosecretkey
