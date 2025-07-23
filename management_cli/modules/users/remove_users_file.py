from management_cli.modules import ModuleBase


class RemoveUsersFileModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Remove User's File"

    def action(self):
        user_name = input("username > ")
        user = self.helper.get_user(user_name)

        if not user:
            print(f"'{user_name}' doesn't exist")
            return

        print(f"files count: {len(user.files)}\n")

        file_uuid = input("file uuid > ")
        self.helper.remove_file(file_uuid=file_uuid, user_id=user.id)

        print(f"{file_uuid} removed.")
