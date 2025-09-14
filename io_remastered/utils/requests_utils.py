import os
from flask import Request, Response
from io_remastered import models
from io_remastered.extra_modules.zip_on_the_fly import ZipFileItemDetails, ZipGenerator


def is_js_request(request: Request):
    return request.headers.get("X-Is-JS-Request", False)


def send_directory_as_zip(directory: models.Directory, user_storage_path: str):
    files_details = []

    for file in directory.files:
        file_path = os.path.join(user_storage_path, file.uuid)
        file_details = ZipFileItemDetails(path=file_path, name=file.name)

        files_details.append(file_details)

    zip_generator = ZipGenerator(files=files_details)

    return Response(zip_generator.generator(), mimetype="application/zip", headers={
        "Content-Disposition": f"attachment; filename={directory.name}.zip"
    })
