from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput


class LoginForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(url="/login", method="POST", csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        self.add_field(TextInput(id="name", props={}, field_name="name",
                       label="name", required=True))
        self.add_field(PasswordInput(id="password", props={}, field_name="password",
                       label="password", required=True))
