import os
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
    with open(file_path, "wb") as file:
        while True:
            chunk = stream.read(chunk_size)

            if not chunk or len(chunk) <= 0:
                break

            file.write(chunk)
