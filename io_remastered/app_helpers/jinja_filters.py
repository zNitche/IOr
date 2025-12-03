from typing import Any


def formatted_file_size(size: str):
    sizes = ["KB", "MB", "GB"]
    size_bytes = int(size)

    current_size = size_bytes

    for size in sizes:
        current_size = round(current_size / 1000, 2)

        if current_size < 1000:
            return f"{current_size}{size}"

    return f"{size_bytes}B"


def convert_to_dict(list: list[Any], target_dict: dict[str, str]):
    def create_target_dict(list_item: Any):
        d = {}

        for key in target_dict:
            attr_name = target_dict.get(key)

            if attr_name is not None:
                d[key] = getattr(list_item, attr_name)

        return d

    return [create_target_dict(list_item=item) for item in list]
