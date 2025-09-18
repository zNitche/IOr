from io import BufferedIOBase
from zipfile import ZipFile, ZipInfo
from dataclasses import dataclass
import re


@dataclass
class ZipFileItemDetails:
    path: str
    name: str


class ZipFileStream(BufferedIOBase):
    def __init__(self):
        self.__buff = b''

    def write(self, b: bytes):  # type: ignore should be ReadableBuffer from _typeshed
        if self.closed:
            raise Exception("can`t write, stream is closed")

        self.__buff += b

        return len(b)

    def get(self):
        chunk = self.__buff
        self.__buff = b""

        return chunk


class ZipOnTheFly():
    def __init__(self, files: list[ZipFileItemDetails], chunk_size=1_000_000):
        self.files = files
        self.chunk_size = chunk_size

        self.__processed_files_names: list[str] = []

    def __parse_duplicated_filename(self, filename: str):
        if filename not in self.__processed_files_names:
            return filename

        split_filename = filename.split(".")
        name = split_filename[0]

        for processed_file_name in self.__processed_files_names:
            is_copy_match = re.search(rf"{name}_copy\(([0-9_]+)\).", processed_file_name)

            if is_copy_match:
                found = is_copy_match.group(0)
                id = int(found.replace(f"{name}_copy(", "").replace(").", "")) + 1

                return filename.replace(name, f"{name}_copy({id})")
        
        return filename.replace(name, f"{name}_copy(1)")

    def __handle_file(self, zip_file: ZipFile, zip_stream: ZipFileStream,
                      file_path: str, file_name: str):
        
        file_name = self.__parse_duplicated_filename(file_name)

        zip_info = ZipInfo.from_file(
            filename=file_path, arcname=file_name)

        with open(file=file_path, mode="rb") as file_obj:
            with zip_file.open(zip_info, mode="w") as current_zip_file:
                while True:
                    chunk = file_obj.read(self.chunk_size)

                    if not chunk:
                        break

                    current_zip_file.write(chunk)

                    yield zip_stream.get()

        self.__processed_files_names.append(file_name)

    def generator(self):
        with ZipFileStream() as zip_stream:
            with ZipFile(zip_stream, mode="w") as zip_file:
                for file in self.files:
                    yield from self.__handle_file(zip_file=zip_file, zip_stream=zip_stream,
                                                  file_name=file.name, file_path=file.path)

            # drain stream
            yield zip_stream.get()
