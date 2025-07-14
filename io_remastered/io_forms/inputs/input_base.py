from typing import Literal, Any
from io_remastered.io_forms.inputs.input_label import InputLabel

INPUT_TYPES = Literal[
    "text",
    "password"
]


class InputBase:
    def __init__(self, id: str, field_name: str, label: str | None,
                 input_type: INPUT_TYPES | None, props: dict[str, Any], required: bool):

        self.input_type = input_type

        self.id = id
        self.props = props
        self.field_name = field_name

        self.required = required

        self.__input_label = InputLabel(input_id=id, label=label) if label else None    

    def __html__(self) -> str | None:
        self.props["id"] = self.id
        self.props["name"] = self.field_name
        self.props["type"] = self.input_type

        return f'<input {self.__render_props()} {'required' if self.required else ''} />'
    
    @property
    def label(self):
        return self.__input_label

    def __render_props(self):
        return " ".join(f'{key}="{self.props[key]}"' for key in self.props)
        
