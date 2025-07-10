from io_remastered.db import Database, migrations
from config.app_config import AppConfig


def main():
    db = Database()
    db.setup(AppConfig.DATABASE_URI)

    if db.engine is None:
        raise Exception("can't create database engine, exiting...")

    migrations.init_migrations(AppConfig.MIGRATIONS_DIR_PATH, db.engine)
    migrations.migrate(AppConfig.MIGRATIONS_DIR_PATH, db.engine)


if __name__ == '__main__':
    main()
