from management_cli.modules import ModuleBase


class RemoveUserFilesModule(ModuleBase):
    def __init__(self, helper):
        super().__init__(helper=helper)

        self.name = "Remove User's Files"

    def action(self):
        user_name = input("username > ")
        user = self.helper.get_user(user_name)

        if not user:
            print(f"'{user_name}' doesn't exist")
            return

        print(f"files count: {len(user.files)}\n")

        for file in user.files:
            self.helper.remove_file(file_uuid=file.uuid, user_id=user.id)

            print(f"{file.uuid} removed.")

        print("done.")
