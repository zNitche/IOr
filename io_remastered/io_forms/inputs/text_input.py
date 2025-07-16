from typing import Any
from io_remastered.io_forms.inputs import InputBase


class TextInput(InputBase):
    def __init__(self, id: str, props: dict[str, Any], field_name: str, label: str | None = None,
                 required: bool = False, placeholder: str | None = None):
        super().__init__(id=id, field_name=field_name, label=label,
                         props=props, input_type="text", required=required, placeholder=placeholder)
