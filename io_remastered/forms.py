from io_remastered import i18n
from io_remastered.io_forms import Form
from io_remastered.io_forms.inputs import TextInput, PasswordInput
from io_remastered.io_forms.validators import DataRequiredValidator, MaxLengthValidator


class LoginForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        name_input = TextInput(id="name", props={"maxlength": 20}, field_name="name",
                               required=True, placeholder=i18n.t("login_form.name"))

        name_input.add_validator(
            DataRequiredValidator(error_message=i18n.t("login_form.validation.field_required")))
        name_input.add_validator(MaxLengthValidator(
            error_message=i18n.t("login_form.validation.max_length_error", {"field": "name", "characters_count": 20}), length=20))

        password_input = PasswordInput(id="password", props={"maxlength": 64}, field_name="password",
                                       required=True, placeholder=i18n.t("login_form.password"))

        password_input.add_validator(
            DataRequiredValidator(error_message=i18n.t("login_form.validation.field_required")))
        password_input.add_validator(MaxLengthValidator(
            error_message=i18n.t("login_form.validation.max_length_error", {"field": "password", "characters_count": 64}), length=64))

        self.add_field(name_input)
        self.add_field(password_input)


class SearchBarForm(Form):
    def __init__(self, search_phrase: str | None):
        super().__init__(csrf_token=None, form_data={
            "search-phrase": search_phrase if search_phrase else ""})

    def setup(self):
        search_phrase_input = TextInput(id="search-phrase", props={"maxlength": 64}, field_name="search",
                                        required=False, placeholder=i18n.t("search_form.search"))

        self.add_field(search_phrase_input)


class CreateDirectoryForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        name_input = TextInput(id="name", props={"maxlength": 32}, field_name="name",
                               required=True, placeholder=i18n.t("create_directory_form.name"))

        name_input.add_validator(
            DataRequiredValidator(error_message=i18n.t("create_directory_form.validation.field_required")))

        self.add_field(name_input)


class RenameStorageItemForm(Form):
    def __init__(self, csrf_token: str | None = None, name: str | None = None):
        super().__init__(csrf_token=csrf_token,
                         form_data={"name": name if name else ""})

    def setup(self):
        name_input = TextInput(id="name", props={"maxlength": 32}, field_name="name",
                               required=True, placeholder=i18n.t("rename_storage_item_form.name"))

        name_input.add_validator(
            DataRequiredValidator(error_message=i18n.t("rename_storage_item_form.validation.field_required")))

        self.add_field(name_input)


class ChangePasswordForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        max_password_length = 64

        data_required_validator = DataRequiredValidator(
            error_message=i18n.t("change_password_page.validation.field_required"))
        max_length_validator = MaxLengthValidator(
            error_message=i18n.t("change_password_page.validation.max_length_error",
                                 {"characters_count": max_password_length}), length=max_password_length)

        password_input = PasswordInput(id="password", props={"maxlength": max_password_length},
                                       field_name="password", required=True,
                                       placeholder=i18n.t("change_password_page.password"))

        new_password_input = PasswordInput(id="new_password", props={"maxlength": max_password_length},
                                           field_name="new_password", required=True,
                                           placeholder=i18n.t("change_password_page.new_password"))

        confirm_new_password_input = PasswordInput(id="confirm_password", props={"maxlength": max_password_length},
                                                   field_name="confirm_password", required=True,
                                                   placeholder=i18n.t("change_password_page.confirm_password"))

        password_input.add_validator(data_required_validator)
        password_input.add_validator(max_length_validator)

        new_password_input.add_validator(data_required_validator)
        new_password_input.add_validator(max_length_validator)

        confirm_new_password_input.add_validator(data_required_validator)
        confirm_new_password_input.add_validator(max_length_validator)

        self.add_field(password_input)
        self.add_field(new_password_input)
        self.add_field(confirm_new_password_input)


class PasswordAuthenticationForm(Form):
    def __init__(self, csrf_token: str | None = None, form_data: dict[str, str] | None = None):
        super().__init__(csrf_token=csrf_token, form_data=form_data)

    def setup(self):
        password_input = PasswordInput(id="password", props={"maxlength": 64}, field_name="password",
                                       required=True, placeholder=i18n.t("password_authentication_page.password"))

        password_input.add_validator(
            DataRequiredValidator(error_message=i18n.t("password_authentication_page.validation.field_required")))
        password_input.add_validator(MaxLengthValidator(
            error_message=i18n.t("password_authentication_page.validation.max_length_error",
                                 {"field": "password", "characters_count": 64}), length=64))

        self.add_field(password_input)
