import socket
import time


def wait_for_db(db_tcp_addr: str, db_tcp_port: int) -> None:
    for _ in range(100):
        try:
            connection = socket.create_connection(
                (db_tcp_addr, db_tcp_port),
                timeout=1,
            )
            connection.close()
            return
        except socket.timeout:
            pass
        except socket.error:
            # In the case of an instant failure (like connection refused) we
            # want to delay slightly before trying again
            time.sleep(0.5)
