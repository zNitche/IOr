from management_cli.helper import Helper


class ModuleBase:
    def __init__(self, helper: Helper):
        self.helper = helper
        self.name = ""

    def show(self):
        pass

    def action(self):
        pass
