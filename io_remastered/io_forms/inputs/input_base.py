from typing import Literal, Any
from io_remastered.io_forms.inputs.input_label import InputLabel
from io_remastered.io_forms.validators import ValidatorBase
from io_remastered.io_forms.field_error import FieldError

INPUT_TYPES = Literal[
    "text",
    "password"
]


class InputBase:
    def __init__(self, id: str, field_name: str,
                 input_type: INPUT_TYPES | None, props: dict[str, Any], label: str | None = None,
                 required: bool = False, placeholder: str | None = None, value: str | None = None):

        self.input_type = input_type

        self.id = id
        self.props = props
        self.field_name = field_name

        self.required = required

        self.value = value
        self.placeholder = placeholder

        self.__input_label = InputLabel(
            input_id=id, label=label) if label else None

        self.__validators: list[ValidatorBase] = []
        self.__validation_errors: list[FieldError] = []

        self.value: str | None = None
        self.is_valid = False

    def __html__(self) -> str | None:
        self.props["id"] = self.id
        self.props["name"] = self.field_name
        self.props["type"] = self.input_type
        self.props["placeholder"] = self.placeholder
        self.props["value"] = self.value

        return f'<input {self.__render_props()} {'required' if self.required else ''} />'

    @property
    def label(self):
        return self.__input_label if self.__input_label else ""

    @property
    def errors(self):
        return self.__validation_errors

    def __render_props(self):
        props = []

        for key, value in self.props.items():
            if value:
                props.append(f'{key}="{value}"')

        return " ".join(props)

    def add_validator(self, validator: ValidatorBase):
        self.__validators.append(validator)

    def validate(self):
        valid = True

        for validator in self.__validators:
            if not validator.validate(self.value):
                self.__validation_errors.append(
                    FieldError(value=self.value, message=validator.error_message))

                valid = False
                break

        self.is_valid = valid
