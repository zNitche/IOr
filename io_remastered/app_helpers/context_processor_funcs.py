from flask import url_for
from datetime import datetime
from io_remastered.models import User
from io_remastered.app_helpers.common_files_extensions import MEDIA_FILE, IMAGE_FILE, CODE_FILE, DOCUMENT_FILE, common_files_extensions


def get_static_resource(path: str):
    return url_for('static', filename=path)


def icon_for_file_extension(extension: str):
    defaut_icon = "file_icon.svg"
    icon_per_type = {
        MEDIA_FILE: "media_file_icon.svg",
        IMAGE_FILE: "graphic_file_icon.svg",
        CODE_FILE: "code_file_icon.svg",
        DOCUMENT_FILE: "document_file_icon.svg",
    }

    icon_type_for_extension = common_files_extensions.get(extension, None)

    if icon_type_for_extension and icon_type_for_extension in icon_per_type.keys():
        return url_for('static', filename=f"icons/{icon_per_type.get(icon_type_for_extension)}")

    return url_for('static', filename=f"icons/{defaut_icon}")


def unpack_dict(input_dict: dict, ommited_keys: list[str]):
    output_dict = {}

    for key in input_dict:
        if key not in ommited_keys:
            output_dict[key] = input_dict[key]

    return output_dict


def is_viewed_by_owner(obj: object, owner: User | None, owner_id_attr_name: str = "owner_id"):
    if owner is None:
        return

    if hasattr(obj, owner_id_attr_name):
        return getattr(obj, owner_id_attr_name) == owner.id

    return False


def parse_iso_date(date_str: str):
    return datetime.fromisoformat(date_str)
