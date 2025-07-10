from management_cli.modules import ModuleBase


class ListUsersModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "List users"

    def show(self):
        print(f"---{self.name}---\n")

    def action(self):
        users_names = self.helper.get_users_names()

        if len(users_names) == 0:
            print("no users to be listed...")

        else:
            for id, name in enumerate(users_names):
                print(f"{id + 1}) {name}")
