from management_cli.modules import ModuleBase


class ListUsersModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "List users"

    def action(self):
        users = self.helper.get_users()

        if len(users) == 0:
            print("no users to be listed...")

        else:
            for user in users:
                print(str(user))
