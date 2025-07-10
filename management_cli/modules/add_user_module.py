from management_cli.modules import ModuleBase


class AddUserModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Add user"

    def action(self):
        user_name = input("username > ")
        password = input("password > ")

        self.helper.add_user(user_name, password)

        print("done")
