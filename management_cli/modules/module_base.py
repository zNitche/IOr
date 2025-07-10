from management_cli.helper import Helper


class ModuleBase:
    def __init__(self, helper: Helper):
        self.helper = helper
        self.name = ""

    def show(self):
        if self.name:
            print(f"---{self.name}---\n")

    def action(self):
        pass
