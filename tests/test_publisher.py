from unittest import TestCase
from unittest.mock import Mock

from pirssi.publisher import Publisher


class TestPublisher(TestCase):
    def test_can_create_connection(self):
        mock_connection = Mock()
        publisher = Publisher(connection=mock_connection)

        publisher.connect()

        mock_connection.connect.assert_called()

    def test_can_publish_message(self):
        mock_connection = Mock()
        publisher = Publisher(connection=mock_connection)

        publisher.publish("I am alive")

        mock_connection.send_message.assert_called_with('{"message": "I am alive"}')

    def test_can_close_connection(self):
        mock_connection = Mock()
        publisher = Publisher(connection=mock_connection)

        publisher.close()

        mock_connection.close.assert_called()
