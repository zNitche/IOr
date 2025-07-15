from io_remastered.io_forms.inputs import InputBase, CSRFTokenField


class Form:
    def __init__(self, csrf_token: str | None,
                 form_data: dict[str, str] | None = None):

        self.csrf_token = csrf_token
        self.form_data = form_data

        self.__fields: list[InputBase] = []

        self.setup()
        self.__fill_fields_values()

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
        raise NotImplementedError()
    
    def __fill_fields_values(self):
        if self.form_data:
            for field in self.__fields:
                field.value = self.form_data.get(field.id)

    def is_valid(self):
        if not self.form_data:
            return False

        for field in self.__fields:
            field.validate()

            if not field.is_valid:
                return False
                
        return True
