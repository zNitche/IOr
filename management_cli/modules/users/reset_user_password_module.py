from getpass import getpass
from management_cli.modules import ModuleBase


class ResetUserPasswordModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Reset User Password"

    def action(self):
        target_username = input("username > ")
        new_password = getpass("password > ")
        
        self.helper.reset_user_password(target_username, new_password)

        print("done")
