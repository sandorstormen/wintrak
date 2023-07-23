from enum import IntEnum
from multiprocessing.connection import Listener, Client
from typing import Any, Optional, Tuple
from signal import signal, SIGTERM, SIGINT


class PortMap(IntEnum):
    TIMER = 6000
    FRONTEND = 6001


class Sender:
    def __init__(self, port: Tuple[str, int], authkey: Optional[bytes] = None) -> None:
        self.port = port
        self.address = ("localhost", self.port)
        self.authkey = authkey
        self.conn = Client(self.address, authkey=self.authkey)
        self.exit_handler = signal(SIGTERM, self.close)
        self.exit_handler = signal(SIGINT, self.close)

    def __del__(self) -> None:
        self.conn.close()

    def send(self, object: Any) -> None:
        self.conn.send(object)

    def close(self) -> None:
        self.conn.close()


class Receiver:
    def __init__(self, port: Tuple[str, int], authkey: Optional[bytes] = None) -> None:
        self.port = port
        self.address = ("localhost", self.port)
        self.authkey = authkey
        self.conn_pool = Listener(self.address, authkey=self.authkey)
        self.exit_handler = signal(SIGTERM, self.close)
        self.exit_handler = signal(SIGINT, self.close)

    def __del__(self) -> None:
        self.conn.close()

    def accept(self) -> Any:
        if hasattr(self, "conn"):
            return self.conn
        else:
            self.conn = self.conn_pool.accept()
            return self.conn

    def recieve(self) -> Any:
        conn = self.accept()
        return conn.recv()

    def close(self) -> None:
        self.conn.close()
