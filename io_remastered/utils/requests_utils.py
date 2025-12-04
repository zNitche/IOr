import os
from flask import Request, Response
from io_remastered import models
from io_remastered.app_helpers.files_responses import WEB_PREVIEW_MIMETYPE_FOR_FILE_EXTENSION
from io_remastered.extra_modules.zip_on_the_fly import ZipFileItemDetails, ZipOnTheFly
from io_remastered.utils import files_utils


def is_js_request(request: Request):
    return request.headers.get("X-Is-JS-Request", False)


def send_directory_as_zip(directory: models.Directory, user_storage_path: str):
    files_details = []

    for file in directory.files:
        file_path = os.path.join(user_storage_path, file.uuid)
        file_details = ZipFileItemDetails(path=file_path, name=file.name)

        files_details.append(file_details)

    zip_on_the_fly = ZipOnTheFly(files=files_details)

    return Response(zip_on_the_fly.generator(), mimetype="application/zip", headers={
        "Content-Disposition": f"attachment; filename={directory.name}.zip"
    })


def stream_media_file(range_header: str, file_path: str, file_size: int,
                      mimetype: str, chunk_size: int = 2_000_000):

    if not mimetype:
        return Response(status=400)

    split_range_header = range_header.split("=")
    split_ranges_part = split_range_header[1].split("-")

    chunk_start = int(split_ranges_part[0])

    chunk_end = min(
        chunk_start + chunk_size, file_size - 1)

    headers = {
        "Content-Range": f"bytes {chunk_start}-{chunk_end}/{file_size}",
        "Accept-Ranges": "bytes",
        "Content-Length": chunk_end - chunk_start + 1,
        "Content-Type": mimetype,
    }

    file_chunk = files_utils.get_file_chunk(
        file_path, chunk_start, chunk_size)

    return Response(file_chunk, headers=headers, status=206)
