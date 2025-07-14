from io_remastered.io_forms.inputs import InputBase, CSRFTokenField


class Form:
    def __init__(self, csrf_token: str | None,
                 form_data: dict[str, str] | None = None):

        self.csrf_token = csrf_token
        self.form_data = form_data

        self.__fields: list[InputBase] = []

        self.setup()

    @property
    def csrf_token_field(self):
        if not self.csrf_token:
            return ""
        
        return CSRFTokenField(token=self.csrf_token)
    
    @property
    def fields(self):
        return self.__fields

    def add_field(self, field: InputBase):
        self.__fields.append(field)

    def setup(self) -> None:
        pass

    def is_valid(self):
        print(self.form_data)
