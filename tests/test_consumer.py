from unittest import TestCase
from unittest.mock import Mock

from pirssi.consumer import Consumer


class TestConsumer(TestCase):

    def test_consumer_can_create_connection(self):
        mock_connection = Mock()
        consumer = Consumer(connection=mock_connection)

        consumer.connect()

        mock_connection.connect.assert_called()

    def test_consumer_can_read(self):
        mock_connection = Mock()
        consumer = Consumer(connection=mock_connection)

        consumer.read_messages()

        mock_connection.read_messages.assert_called()
