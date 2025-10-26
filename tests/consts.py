from uuid import uuid4


class UsersConsts:
    TEST_USER_NAME = "user"
    TEST_USER_PASSWORD = "pass123"


class StorageConsts:
    SHARED_FILE_SHARE_UUID = uuid4().hex
    SHARED_DIRECTORY_SHARE_UUID = uuid4().hex
