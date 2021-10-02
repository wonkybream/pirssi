import json

from pirssi.connection import Connection


class Publisher:

    _connection: Connection

    def __init__(self, connection: Connection):
        self._connection = connection

    def connect(self):
        self._connection.connect()

    def publish(self, message: str):
        json_message = json.dumps({"message": message})
        self._connection.send_message(json_message)

    def close(self):
        self._connection.close()
