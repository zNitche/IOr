import os
from management_cli.modules import ModuleBase, ExitModule, ListUsersModule
from management_cli.helper import Helper


class CLI:
    def __init__(self):
        self.modules = self.init_modules()

    def init_modules(self):
        helper = Helper()
        modules: list[type[ModuleBase]] = [
            ExitModule, ListUsersModule
        ]

        return [module(helper=helper) for module in modules]

    def mainloop(self):
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
