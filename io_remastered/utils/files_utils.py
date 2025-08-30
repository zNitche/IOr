import os
import hashlib
from typing import IO


def get_file_size(file_path: str):
    stats = os.stat(file_path)
    return stats.st_size


def get_directory_files_size(files_path: str):
    size = 0

    for file in os.listdir(files_path):
        file_path = os.path.join(files_path, file)
        size += get_file_size(file_path)

    return size


def write_file_from_stream(stream: IO[bytes], file_path: str, chunk_size=102400):
    if not os.path.exists(file_path):
        raise Exception(f"file '{file_path}' doesn't exists")

    with open(file_path, "ab") as file:
        while True:
            chunk = stream.read(chunk_size)

            if not chunk or len(chunk) <= 0:
                break

            file.write(chunk)


def get_filename_for_tmp_upload(uuid: str, user_id: int):
    return f"{uuid}_{user_id}"


def create_tmp_file_for_upload(tmp_files_path: str, uuid: str, user_id: int):
    path = os.path.join(
        tmp_files_path, get_filename_for_tmp_upload(uuid, user_id))

    if os.path.exists(path):
        os.remove(path)

    open(path, "x").close()


def get_sha256sum_for_file(file_path: str):
    if not os.path.exists(file_path):
        raise Exception(f"file '{file_path}' doesn't exists")

    with open(file_path, "rb") as file:
        sha256_hash = hashlib.file_digest(file, "sha256")

    return sha256_hash.hexdigest()
