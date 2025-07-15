from io_remastered.io_forms.validators import ValidatorBase


class MinLengthValidator(ValidatorBase):
    def __init__(self, length: int, error_message: str):
        super().__init__(error_message=error_message)

        self.length = length

    def validate(self, value: str):
        return False if value and len(value) < self.length else True
