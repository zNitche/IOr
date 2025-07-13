from typing import Literal
from io_remastered.io_forms.inputs import InputBase


class Form:
    def __init__(self, url: str, method: Literal["GET", "POST"], submit_button_text: str, csrf_token: str | None):
        self.url = url
        self.method = method
        self.submit_button_text = submit_button_text

        self.csrf_token = csrf_token

        self.__inputs: list[InputBase] = []

    def add_input(self, input: InputBase):
        self.__inputs.append(input)

    def setup(self) -> None:
        pass

    def __get_merged_inputs(self):
        struct = []

        for input in self.__inputs:
            struct.append(input.render())

        return "\n".join(struct)

    def __render_submit_button(self):
        return f'<input type="submit" value="{self.submit_button_text}" />'

    def render(self):
        struct = []

        struct.append(f'<form action="{self.url}" method="{self.method}">')

        if self.csrf_token:
            struct.append(f'<input hidden value="{self.csrf_token}" name="csrf_token" />')

        struct.append(self.__get_merged_inputs())
        struct.append(self.__render_submit_button())
        struct.append('</form>')

        return "\n".join(struct)
