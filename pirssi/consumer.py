from typing import Callable

from pirssi.connection import Connection
from pirssi.handler import Handler


class Consumer:
    _connection: Connection
    _handler = Handler = Handler()

    def __init__(self, connection: Connection):
        self._connection = connection

    def connect(self):
        self._connection.connect()

    def read_messages(self):
        messages = self._connection.read_messages()
        for message in messages:
            self._handler(message)

    def close(self):
        self._connection.close()

    def add_handler(self, handler: Callable):
        self._handler.append(handler)
