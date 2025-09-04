from io_remastered.models import File, User, Directory


def is_file_accessible(file: File, user: User):
    is_owner = file.owner_id == user.id
    accessible = file.directory and (file.directory.is_shared or is_owner)
    
    return bool(accessible)


def is_directory_accessible(directory: Directory, user: User):
    accessible = directory.is_shared or (directory.owner_id == user.id)
    
    return bool(accessible)
