import logging
import secrets

import socket
from time import sleep

logger = logging.getLogger(__name__)


class Connection:
    _socket: socket
    _username: str = f"pirssi-{secrets.token_hex(6)}"
    _message_prefix: str = ":pirssi:"

    _channel: str
    _server: str
    _server_port: int
    _channel: str
    _connection_timeout: int

    def __init__(
            self,
            server: str = "irc.quakenet.org",
            server_port: int = 6667,
            channel: str = "#pirssi-queue",
            connection_timeout: int = 30
    ):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server = server
        self._server_port = server_port
        self._channel = channel
        self._connection_timeout = connection_timeout

    def connect(self):
        logger.info(f"Connecting to {self._server}:{self._server_port} channel {self._channel}")
        self._socket.connect((self._server, self._server_port))

        self._send("USER", f"{self._username} . . :pirssi")
        self._send("NICK", self._username)

        self._wait_for_ident_challenge()
        self._wait_for_message_of_the_day()

    def _wait_for_ident_challenge(self):
        cycles = 0
        while cycles < self._connection_timeout:
            logger.info(f"Waiting for ident message... elapsed {cycles}s")
            reply_buffer = self._socket.recv(4096).decode("utf-8")

            if "PING" in reply_buffer:
                ident_response = [line for line in reply_buffer.splitlines() if "PING" in line][0]
                self._send("PONG", f"{ident_response.split()[1]}")
                break

            sleep(1)
            cycles += 1

    def _wait_for_message_of_the_day(self):
        cycles = 0
        while cycles < self._connection_timeout:
            logger.info(f"Waiting for message of the day... elapsed {cycles}s")
            reply_buffer = self._socket.recv(4096).decode("utf-8")

            if "Message of the Day" in reply_buffer:
                self._send("JOIN", self._channel)
                break
            sleep(1)
            cycles += 1

    def _send(self, command: str, message: str):
        self._socket.send(f"{command} {message}\r\n".encode())

    def send_message(self, message: str):
        self._send("PRIVMSG", f"{self._channel} : {self._message_prefix}{message}")

    def close(self):
        logger.info("Closing connection")
        self._send("QUIT", "")
        self._socket.shutdown(1)
        self._socket.close()
