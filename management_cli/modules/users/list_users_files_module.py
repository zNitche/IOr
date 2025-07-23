from management_cli.modules import ModuleBase


class ListUsersFilesModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "List User Files"

    def action(self):
        user_name = input("username > ")
        user = self.helper.get_user(user_name)

        if not user:
            print(f"'{user_name}' doesn't exist")
            return
        
        print(f"files count: {len(user.files)}\n")

        for file in user.files:
            print(self.helper.cleanup_db_object(file))
