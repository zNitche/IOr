from io_remastered.io_forms.validators import ValidatorBase


class DataRequiredValidator(ValidatorBase):
    def __init__(self, error_message: str):
        super().__init__(error_message=error_message)

    def validate(self, value):
        return False if not value else True
