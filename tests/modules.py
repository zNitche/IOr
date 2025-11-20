import threading
import time
from whimdb import Server, Client


def get_whimdb_server(port=8080):
    server = Server(port=port)

    thread = threading.Thread(target=server.start)
    thread.start()

    client = get_whimdb_client(port=port)

    while True:
        res = client.echo()

        if res:
            break

        time.sleep(1)

    return server, thread


def stop_whimdb_server(server: Server, thread: threading.Thread):
    server.stop()
    thread.join()


def get_whimdb_client(port=8080):
    return Client(database_id=0, addr="0.0.0.0", port=port)
