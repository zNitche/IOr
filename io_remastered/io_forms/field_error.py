class FieldError:
    def __init__(self, value: str | None, message: str):
        self.value = value
        self.message = message

    def __str__(self):
        return self.message
