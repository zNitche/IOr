from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput


class LoginForm(Form):
    def __init__(self):
        super().__init__(url="/login", method="POST", submit_button_text="login")

        self.setup()

    def setup(self):
        self.add_input(TextInput(props={}, field_name="name",
                       label="name", required=True))
        self.add_input(PasswordInput(props={}, field_name="password",
                       label="password", required=True))
