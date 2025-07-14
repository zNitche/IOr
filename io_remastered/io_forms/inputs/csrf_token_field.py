class CSRFTokenField:
    def __init__(self, token: str):
        self.token = token

    def __html__(self):
        return f'<input hidden name="csrf_token" value="{self.token}" />'
