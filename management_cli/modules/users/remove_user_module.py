from management_cli.modules import ModuleBase


class RemoveUserModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Remove User"

    def show(self):
        return

    def action(self):
        username = input("username > ")
        self.helper.delete_user(username)

        print("done")
