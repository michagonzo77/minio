from pydantic import BaseModel
from typing import List, Literal

class ListBucketsInput(BaseModel):
    pass

options_dict = {"read":"s3:ListBucket",
           "write":"s3:PutObject", "delete":"s3:DeleteObject", "get":"s3:GetObject", "location":"s3:GetBucketLocation", "list_parts":"s3:ListMultipartUploadParts",
           "abort_upload":"s3:AbortMultipartUpload", "list_uploads":"s3:ListBucketMultipartUploads"}

OptionalPaths = Literal[*options_dict.keys()]

class CreateBucketPermission(BaseModel):
    bucket_name: str
    permission_type: List[OptionalPaths]

class CreateBucket(BaseModel):
    bucket_name: str

class DeleteBucket(BaseModel):
    bucket_name: str

class GetBucketPolicy(BaseModel):
    bucket_name: str

class ListObjects(BaseModel):
    bucket_name: str

class GetObjectLink(BaseModel):
    bucket_name: str
    object_name: str
    expiration_time_hours: int

class CreateUser(BaseModel):
    access_key: str
    secret_key: str

class DeleteUser(BaseModel):
    access_key: str

class DisableUser(BaseModel):
    access_key: str

class EnableUser(BaseModel):
    access_key: str

class ListGroups(BaseModel):
    pass

class AddMembersToGroup(BaseModel):
    group_name: str
    members: list

class DeleteGroup(BaseModel):
    group_name: str

class AddBucketQuota(BaseModel):
    bucket_name: str
    size: str

type_dict = {"type_user":"user", "type_group":"group"}
policies_dict = {"policy_readonly":"readonly",
                 "policy_readwrite":"readwrite",
                 "policy_diagnostics":"diagnostics",
                 "policy_writeonly":"writeonly"}

OptionalTypes = Literal[*type_dict.keys()]
OptionalPolicies = Literal[*policies_dict.keys()]

class AttachPolicy(BaseModel):
    type: OptionalTypes
    policy: OptionalPolicies
    name_of_user_or_group: str

class ListUsers(BaseModel):
    pass

class UserInfo(BaseModel):
    username: str

class GroupInfo(BaseModel):
    group_name: str