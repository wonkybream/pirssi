import socket
from unittest import TestCase
from unittest.mock import patch, Mock, call

from pirssi.connection import Connection


class TestConnection(TestCase):

    @patch("pirssi.connection.socket.socket")
    def test_sets_up_stream_socket_over_ip4(self, mock_socket):
        Connection()

        mock_socket.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    def test_uses_correct_server_and_port(self):
        connection = Connection(
            server="I am IRC server",
            server_port=6667,
            connection_timeout=0)
        mock_socket = Mock()
        connection._socket = mock_socket

        connection.connect()

        mock_socket.connect.assert_called_with(("I am IRC server", 6667))

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    def test_sends_user_before_nick(self):
        connection = Connection(connection_timeout=0)
        mock_socket = Mock()
        connection._socket = mock_socket
        connection._username = "pirssi-bot"

        connection.connect()

        mock_socket.send.assert_has_calls([
            call(b'USER pirssi-bot . . :pirssi\r\n'),
            call(b'NICK pirssi-bot\r\n')
        ])

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    @patch("pirssi.connection.Connection._wait_for_ident_challenge")
    def test_waits_for_ident_challenge(self, mock_ident_challenge):
        connection = Connection(connection_timeout=0)
        connection._socket = Mock()

        connection.connect()

        mock_ident_challenge.assert_called()

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    @patch("pirssi.connection.Connection._wait_for_message_of_the_day")
    def test_waits_for_message_of_the_day(self, mock_message_of_the_day):
        connection = Connection(connection_timeout=0)
        connection._socket = Mock()

        connection.connect()

        mock_message_of_the_day.assert_called()

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    def test_responds_to_ident_challenge(self):
        connection = Connection(connection_timeout=1)
        mock_socket = Mock()
        connection._socket = mock_socket
        mock_socket.recv.return_value = b"PING 123456"

        connection._wait_for_ident_challenge()

        mock_socket.send.assert_called_with(b"PONG 123456\r\n")

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    def test_joins_to_channel_after_message_of_the_day_reply(self):
        connection = Connection(connection_timeout=1, channel="#some-irc-channel")
        mock_socket = Mock()
        connection._socket = mock_socket
        mock_socket.recv.return_value = b"Message of the Day"

        connection._wait_for_message_of_the_day()

        mock_socket.send.assert_called_with(b"JOIN #some-irc-channel\r\n")

    @patch("pirssi.connection.socket.socket", lambda x, y: None)
    def test_sends_message_to_channel(self):
        connection = Connection(connection_timeout=0, channel="#another-irc-channel")
        mock_socket = Mock()
        connection._socket = mock_socket
        connection._message_prefix = ":prefix:"

        connection.send_message("I am message")

        mock_socket.send.assert_called_with(b"PRIVMSG #another-irc-channel ::prefix:I am message\r\n")
