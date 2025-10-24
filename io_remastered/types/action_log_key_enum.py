from enum import Enum

class ActionLogKeyEnum(Enum):
    FileUploaded = "file_uploaded"
    FileRemoved = "file_removed"
    DirectoryCreated = "directory_created"
    FileRenamed = "file_renamed"
    DirectoryRemoved = "directory_removed"
    DirectoryRenamed = "directory_renamed"
    ToggledDirectorySharing = "toggled_directory_sharing"
