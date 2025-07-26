from getpass import getpass
from management_cli.modules import ModuleBase


class AddUserModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Add user"

    def action(self):
        user_name = input("username > ")
        password = getpass("password > ")
        confirm_new_password = getpass("confirm password > ")

        if password != confirm_new_password:
            raise Exception("passwords doesn't match")

        storage_size = int(input("storage size (in GB) > "))

        self.helper.add_user(user_name=user_name,
                             password=password, storage_size=storage_size)

        print("done")
