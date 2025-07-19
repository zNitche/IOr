from management_cli.modules import ModuleBase


class ChangeUserMaxStorageSize(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Change User Max Storage Size"

    def action(self):
        user_name = input("username > ")
        storage_size = int(input("storage size (in GB) > "))

        self.helper.change_user_max_storage_size(
            user_name=user_name, storage_size=storage_size)

        print("done")
