from typing import Any


class ValidatorBase:
    def __init__(self, error_message):
        self.error_message = error_message

    def validate(self, value: Any) -> bool:
        raise NotImplementedError()
