class InputLabel:
    def __init__(self, input_id: str, label: str):
        self.input_id = input_id
        self.label = label

    def __html__(self):
        return f'<label for="{self.input_id}">{self.label}</label>'
