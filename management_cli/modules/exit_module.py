from management_cli.modules import ModuleBase
import sys


class ExitModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Exit"

    def action(self):
        print("Exiting, bye...")
        sys.exit()
