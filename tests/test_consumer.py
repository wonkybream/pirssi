from unittest import TestCase
from unittest.mock import Mock, patch, call

from pirssi.consumer import Consumer


class TestConsumer(TestCase):

    def test_can_create_connection(self):
        mock_connection = Mock()
        consumer = Consumer(connection=mock_connection)

        consumer.connect()

        mock_connection.connect.assert_called()

    def test_can_close_connection(self):
        mock_connection = Mock()
        consumer = Consumer(connection=mock_connection)

        consumer.close()

        mock_connection.close.assert_called()

    @patch('pirssi.consumer.Consumer._handler')
    def test_read_messages_are_forwarded_to_handler(self, mock_handler):
        mock_connection = Mock()
        consumer = Consumer(connection=mock_connection)
        mock_connection.read_messages.return_value = [
            "Message number one",
            "Message number two"
        ]

        consumer.read_messages()

        mock_handler.assert_has_calls([
            call("Message number one"),
            call("Message number two")
        ])
