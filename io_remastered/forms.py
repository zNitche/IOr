from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput
from io_remastered.io_forms.validators import MaxLengthValidator, DataRequiredValidator


class LoginForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        name_input = TextInput(id="name", props={}, field_name="name",
                               label="name", required=True)

        name_input.add_validator(
            DataRequiredValidator(error_message="field required"))

        password_input = PasswordInput(id="password", props={}, field_name="password",
                                       label="password", required=True)

        password_input.add_validator(
            DataRequiredValidator(error_message="field required"))

        self.add_field(name_input)
        self.add_field(password_input)
