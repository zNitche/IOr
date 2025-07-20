from getpass import getpass
from management_cli.modules import ModuleBase


class ResetUserPasswordModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Reset User Password"

    def action(self):
        target_username = input("username > ")

        new_password = getpass("password > ")
        confirm_new_password = getpass("confirm password > ")

        if new_password != confirm_new_password:
            raise Exception("passwords doesn't match")
        
        self.helper.reset_user_password(target_username, new_password)

        print("done")
