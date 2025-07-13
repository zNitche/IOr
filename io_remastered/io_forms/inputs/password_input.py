from typing import Any
from io_remastered.io_forms.inputs import InputBase


class PasswordInput(InputBase):
    def __init__(self, props: dict[str, Any], field_name: str, label: str | None, required: bool):
        super().__init__(field_name=field_name, label=label,
                         props=props, input_type="password", required=required)
