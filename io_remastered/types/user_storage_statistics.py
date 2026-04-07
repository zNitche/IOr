from dataclasses import dataclass, field


@dataclass
class ShortStatistics:
    files: int | None = field(default=0)
    directories: int | None = field(default=0)
    shared_files: int | None = field(default=0)
    shared_directories: int | None = field(default=0)
    tmp_files: int | None = field(default=0)

    @property
    def dict(self):
        return self.__dict__


@dataclass
class UserStorageStatistics:
    short_statistics: ShortStatistics = field(default_factory=ShortStatistics)
    has_tmp_files: bool = field(default=False)
    files_count_by_extension: dict[str, int] = field(default_factory=dict)
