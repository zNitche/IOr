from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput


class LoginForm(Form):
    def __init__(self, csrf_token: str | None = None):
        super().__init__(url="/login/action", method="POST",
                         submit_button_text="login", csrf_token=csrf_token)

        self.setup()

    def setup(self):
        self.add_input(TextInput(id="name", props={}, field_name="name",
                       label="name", required=True))
        self.add_input(PasswordInput(id="password", props={}, field_name="password",
                       label="password", required=True))
