from redis import Redis, ConnectionPool
import json
from contextlib import contextmanager


class RedisCacheDatabase:
    def __init__(self, db_id: int):
        self.db_id: int = db_id

        self.server_address: str | None = None
        self.server_port: int | None = None

        self.__connection_pool: ConnectionPool | None = None

    def __create_connection_pool(self):
        self.__connection_pool = ConnectionPool(host=self.server_address, port=self.server_port, db=self.db_id,
                                                decode_responses=True)

    @contextmanager
    def db_session(self, raise_exception=True):
        connection = Redis(connection_pool=self.__connection_pool)

        try:
            yield connection

        except Exception as e:
            if raise_exception:
                raise e

        finally:
            connection.close()

    def setup(self, address: str, port: int, flush=True):
        self.server_address = address
        self.server_port = port

        self.__create_connection_pool()

        if flush:
            self.flush_db()

    def flush_db(self):
        with self.db_session() as session:
            session.flushdb()

    def update_ttl(self, key: str, ttl: int):
        with self.db_session() as session:
            session.getex(key, ex=ttl)

    def set_value(self, key: str, value: dict | str | int | bool, ttl=60):
        with self.db_session() as session:
            session.set(key, json.dumps(value), ex=ttl)

    def get_value(self, key: str | None = None, pattern: str | None = None):
        with self.db_session() as session:
            if key is not None:
                data = session.get(key)

                return json.loads(str(data)) if data else None

            elif pattern is not None:
                for inner_key in session.scan_iter(pattern):
                    if inner_key:
                        data = session.get(inner_key)
                        return json.loads(str(data)) if data else None

        return None
    
    def get_key_for_pattern(self, pattern: str) -> str | None:
        with self.db_session() as session:
            for key in session.scan_iter(pattern):
                return key

    def delete_key(self, key: str | None = None, pattern: str | None = None):
        with self.db_session() as session:
            if key is not None:
                session.delete(key)

            elif pattern is not None:
                for inner_key in session.scan_iter(pattern):
                    session.delete(inner_key)

    def get_all_keys_for_pattern(self, pattern: str):
        keys = []

        with self.db_session() as session:
            for key in session.scan_iter(pattern):
                keys.append(key)

        return keys
