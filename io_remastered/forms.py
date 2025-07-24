from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput
from io_remastered.io_forms.validators import DataRequiredValidator, MaxLengthValidator


class LoginForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        name_input = TextInput(id="name", props={"maxlength": 20}, field_name="name",
                               required=True, placeholder="name")

        name_input.add_validator(
            DataRequiredValidator(error_message="field required"))
        name_input.add_validator(MaxLengthValidator(
            error_message="username can't exceed 20 characters", length=20))

        password_input = PasswordInput(id="password", props={"maxlength": 64}, field_name="password",
                                       required=True, placeholder="password")

        password_input.add_validator(
            DataRequiredValidator(error_message="field required"))
        password_input.add_validator(MaxLengthValidator(
            error_message="password can't exceed 64 characters", length=64))

        self.add_field(name_input)
        self.add_field(password_input)


class SearchBarForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        search_phrase_input = TextInput(id="search-phrase", props={"maxlength": 64}, field_name="search",
                                        required=False, placeholder="search")

        self.add_field(search_phrase_input)
