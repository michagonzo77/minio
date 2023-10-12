from ..connection import  (
    getclient,
    getadminclient,
)
from datetime import timedelta
import json

from ..models.minio_kubiya_models import (
    ListBucketsInput,
    CreateBucketPermission,
    options_dict,
    CreateBucket,
    DeleteBucket,
    GetBucketPolicy,
    ListObjects,
    GetObjectLink,
    CreateUser,
    DeleteUser,
    DisableUser,
    EnableUser,
    ListGroups,
    AddMembersToGroup,
    DeleteGroup,
    AddBucketQuota,
    AttachPolicy,
    type_dict,
    policies_dict,
    ListUsers,
    UserInfo,
    GroupInfo,
)
from . import action_store as action_store


@action_store.kubiya_action()
def list_buckets(input: ListBucketsInput) -> str:
    """An action to list buckets in Minio."""
    client = getclient()
    buckets = client.list_buckets()
    bucket_list = ''
    for bucket in buckets:
        bucket_list += f"\nBucket name: {bucket.name}\nCreated in: {bucket.creation_date}\n"
    if bucket_list == "":
        return "There are no buckets to display."
    return bucket_list


@action_store.kubiya_action()
def create_bucket_policy(input: CreateBucketPermission) -> str:
    """An action to set bucket policies in Minio."""
    client = getclient()
    bucket_permissions = ['s3:ListBucket', 's3:GetBucketLocation', 's3:ListBucketMultipartUploads']
    policy = {
        "Version": "2012-10-17",
        "Statement": []
    }
    for permission_type in input.permission_type:
        if options_dict[permission_type] not in bucket_permissions:
            policy['Statement'].append({
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [options_dict[permission_type]],
                "Resource": f"arn:aws:s3:::{input.bucket_name}/*",
            })
        if options_dict[permission_type] in bucket_permissions:
            policy['Statement'].append({
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": [options_dict[permission_type]],
                "Resource": f"arn:aws:s3:::{input.bucket_name}",
            })
    try:
        client.set_bucket_policy(input.bucket_name, json.dumps(policy))
        return f"Policies: {', '.join(input.permission_type)} set successfully for bucket {input.bucket_name}"
    except Exception as error:
        return f"An error occurred: {error}"
    

@action_store.kubiya_action()
def create_bucket(input: CreateBucket) -> str:
    """Action to create a bucket in Minio"""
    client = getclient()
    client.make_bucket(input.bucket_name)
    try:
        return f"Bucket {input.bucket_name} created successfully!"
    except Exception as error:
        return f"Error creating bucket {input.bucket_name}: {error}"
    

@action_store.kubiya_action()
def delete_bucket(input: DeleteBucket) -> str:
    """Action to delete a bucket in Minio"""
    client = getclient()
    client.remove_bucket(input.bucket_name)
    try:
        return f"Bucket {input.bucket_name} deleted successfully!"
    except Exception as error:
        return f"Error deleting bucket {input.bucket_name}: {error}"


@action_store.kubiya_action()
def get_bucket_policy(input: GetBucketPolicy) -> str:
    """Action to get a bucket's policy in Minio"""
    client = getclient()
    policy = client.get_bucket_policy(input.bucket_name)
    try:
        return f"The bucket {input.bucket_name}'s policy is:\n{policy}"
    except Exception as error:
        return f"Error retrieving bucket {input.bucket_name}'s policy:\n{error}"


@action_store.kubiya_action()
def list_objects(input: ListObjects) -> str:
    """Action to list a bucket's objects in Minio"""
    client = getclient()
    objects = client.list_objects(input.bucket_name)
    final_output = ""
    for obj in objects:
        final_output += obj.object_name + "\n"
    if final_output == "":
        return f"The bucket '{input.bucket_name}' does not contain any objects."
    try:
        return f"Here's the list of objects for the bucket {input.bucket_name}:\n\n{final_output}"
    except Exception as error:
        return f"Error retrieving bucket {input.bucket_name}'s objects:\n{error}"


@action_store.kubiya_action()
def get_object_link_with_expiration_time(input: GetObjectLink) -> str:
    """Action to get a presigned URL to download an object from a bucket with time expiration in Minio"""
    client = getclient()
    url = client.get_presigned_url(
    "GET",
    input.bucket_name,
    input.object_name,
    expires=timedelta(hours=input.expiration_time_hours),
    )
    try:
        return f"Here is the link for the object '{input.object_name}' from the bucket '{input.bucket_name}' with the expiration time of {input.expiration_time_hours} hours:\n\n{url}"
    except Exception as error:
        return f"Error retrieving url for the object '{input.object_name}' from the bucket '{input.bucket_name}' with the expiration time of {input.expiration_time_hours} hours:\n\n{error}"

############################### Minio Admin Client ####################################################################

@action_store.kubiya_action()
def list_users(input: ListUsers) -> str:
    """Action to list all users in Minio"""
    client = getadminclient()
    response = client.list_users()
    return response

@action_store.kubiya_action()
def user_info(input: UserInfo) -> str:
    """Action to display a user's info in Minio"""
    client = getadminclient()
    response = client.user_info(input.username)
    return response

@action_store.kubiya_action()
def create_user(input: CreateUser) -> str:
    """Action to create a user in Minio"""
    client = getadminclient()
    response = client.create_user(input.access_key, input.secret_key)
    return response

@action_store.kubiya_action()
def delete_user(input: DeleteUser) -> str:
    """Action to delete a user in Minio"""
    client = getadminclient()
    response = client.delete_user(input.access_key)
    return response

@action_store.kubiya_action()
def disable_user(input: DisableUser) -> str:
    """Action to disable a user in Minio"""
    client = getadminclient()
    response = client.disable_user(input.access_key)
    return response

@action_store.kubiya_action()
def enable_user(input: EnableUser) -> str:
    """Action to enable a user in Minio"""
    client = getadminclient()
    response = client.enable_user(input.access_key)
    return response

@action_store.kubiya_action()
def list_groups(input: ListGroups) -> str:
    """Action to list groups in Minio"""
    client = getadminclient()
    response = client.list_groups()
    return response

@action_store.kubiya_action()
def group_info(input: GroupInfo) -> str:
    """Action to get the group's information in Minio"""
    client = getadminclient()
    response = client.group_info(input.group_name)
    return response

@action_store.kubiya_action()
def add_members_to_group(input: AddMembersToGroup) -> str:
    """Action to add members to a group in Minio"""
    client = getadminclient()
    response = client.add_members_to_group(input.group_name, input.members)
    return response

@action_store.kubiya_action()
def delete_group(input: DeleteGroup) -> str:
    """Action to delete a group in Minio"""
    client = getadminclient()
    response = client.delete_group(input.group_name)
    return response

@action_store.kubiya_action()
def add_bucket_quota(input: AddBucketQuota) -> str:
    """Action to add a quota to a bucket in Minio"""
    client = getadminclient()
    response = client.add_bucket_quota(input.bucket_name, input.size)
    return response

@action_store.kubiya_action()
def attach_policy(input: AttachPolicy) -> str:
    """Action to attach a policy to a user or group in Minio"""
    client = getadminclient()
    response = client.attach_policy(type_dict[input.type], policies_dict[input.policy], input.name_of_user_or_group)
    return response