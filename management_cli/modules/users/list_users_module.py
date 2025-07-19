from typing import Any
from management_cli.modules import ModuleBase
from io_remastered.models import User


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
                print(self.__cleanup_object(user))
                print("\nFiles:")
                print(user.files)

    
    def __cleanup_object(self, object: Any):
        struct = {}
        dict = object.__dict__

        for key in dict:
            if not key.startswith("_"):
                struct[key] = dict.get(key)

        return struct
