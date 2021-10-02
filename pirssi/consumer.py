from pirssi.connection import Connection


class Consumer:

    _connection: Connection

    def __init__(self, connection: Connection):
        self._connection = connection

    def connect(self):
        self._connection.connect()

    def read_messages(self):
        self._connection.read_messages()
