from typing import Literal, Any


INPUT_TYPES = Literal[
    "text",
    "password"
]


class InputBase:
    def __init__(self, id: str, field_name: str, label: str | None, input_type: INPUT_TYPES, props: dict[str, Any], required: bool):
        self.id = id
        self.input_type = input_type
        self.props = props
        self.field_name = field_name
        self.label = label
        self.required = required

        self.data_struct: list[str | None] = []

    def render_label(self):
        if self.label is None:
            return None

        return f'<label for="{self.id}">{self.label}</label>'

    def merge_content(self):
        filtered_data = []

        for item in self.data_struct:
            if item:
                filtered_data.append(item)

        return "\n".join(filtered_data)
    
    def __render_props(self):
        return " ".join(f'{key}="{self.props[key]}"' for key in self.props)

    def render(self):
        self.props["id"] = self.id
        self.props["name"] = self.field_name
        self.props["type"] = self.input_type

        self.data_struct.append(self.render_label())
        self.data_struct.append(
            f'<input {self.__render_props()} {'required' if self.required else ''} />')

        return self.merge_content()
