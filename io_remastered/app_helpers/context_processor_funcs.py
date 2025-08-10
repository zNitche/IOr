from flask import url_for
from io_remastered.app_helpers.common_files_extensions import MEDIA_FILE, IMAGE_FILE, CODE_FILE, DOCUMENT_FILE, common_files_extensions


def get_static_resource(path: str):
    return url_for('static', filename=path)


def icon_for_file_extension(extension: str):
    defaut_icon = "file_icon.svg"
    icon_per_type = {
        MEDIA_FILE: "media_file_icon.svg",
        IMAGE_FILE: "graphic_file_icon.svg",
        CODE_FILE: "code_file_icon.svg",
        DOCUMENT_FILE: "file_icon.svg",
    }

    icon_type_for_extension = common_files_extensions.get(extension, None)

    if icon_type_for_extension and icon_type_for_extension in icon_per_type.keys():
        return url_for('static', filename=f"icons/{icon_per_type.get(icon_type_for_extension)}") 

    return url_for('static', filename=f"icons/{defaut_icon}") 
