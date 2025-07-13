from typing import Any
from io_remastered.io_forms.inputs import InputBase


class PasswordInput(InputBase):
    def __init__(self, id: str, props: dict[str, Any], field_name: str, label: str | None, required: bool):
        super().__init__(id=id, field_name=field_name, label=label,
                         props=props, input_type="password", required=required)
