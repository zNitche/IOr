import os
from load_dotenv import load_dotenv
from io_remastered.extra_modules import InMemoryDatabase
from io_remastered.tasks_scheduler import TasksSchedulerServer


class TasksSchedulerServerRunner:
    def __init__(self):
        self.__whimdb_server_address = os.getenv("WHIMDB_SERVER_ADDRESS")
        self.__whimdb_server_port = os.getenv("WHIMDB_SERVER_PORT")

        self.__in_memory_database = InMemoryDatabase(db_id=1)

    def run(self):
        if self.__whimdb_server_address is None or self.__whimdb_server_port is None:
            raise Exception("can't connect to in memory database.")

        self.__in_memory_database.setup(
            server_address=self.__whimdb_server_address,
            server_port=int(self.__whimdb_server_port), flush=True)

        server = TasksSchedulerServer(
            broker_db=self.__in_memory_database, max_running_tasks=5,
            mainloop_pooling_interval=5)

        server.run()


if __name__ == "__main__":
    load_dotenv(".env.app")

    runner = TasksSchedulerServerRunner()
    runner.run()
