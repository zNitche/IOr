import os
from management_cli.helper import Helper
from management_cli.modules import ModuleBase
from management_cli.modules import ExitModule
from management_cli.modules.users import ListUsersModule
from management_cli.modules.users import AddUserModule
from management_cli.modules.users import RemoveUserModule
from management_cli.modules.users import ResetUserPasswordModule


class CLI:
    def __init__(self):
        self.modules = self.init_modules()

    def init_modules(self):
        helper = Helper()
        modules: list[type[ModuleBase]] = [
            ExitModule, ListUsersModule, AddUserModule,
            RemoveUserModule, ResetUserPasswordModule
        ]

        return [module(helper=helper) for module in modules]

    def mainloop(self):
        try:
            print("---IOr CLI---\n")
            print("Choose what you want to do: ")

            for id, module in enumerate(self.modules):
                print(f"{id} - {module.name}")

            choice = int(input("> "))
            os.system("clear")

            if 0 <= choice < len(self.modules):
                module = self.modules[choice]

                module.show()
                module.action()

            else:
                print("Unknown option")

            input("\nPress any key to continue")

            self.mainloop()

        except KeyboardInterrupt:
            print("Closing, bye...")
