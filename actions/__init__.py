from kubiya import ActionStore

action_store = ActionStore("minio-kubiya-actions", "0.0.1")

action_store.uses_secrets(["MINIO_HOST", "MINIO_ACCESSKEY", "MINIO_SECRETKEY"])