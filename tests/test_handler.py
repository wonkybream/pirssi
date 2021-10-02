from unittest import TestCase
from unittest.mock import Mock

from pirssi.handler import Handler


def function_without_arguments():
    pass


def function_with_one_argument(one):
    one.called_from_handler = True


def function_with_two_arguments(one, two):
    print(f"{one}:{two}")


class TestHandler(TestCase):

    def test_handler_accepts_function_with_one_argument(self):
        handler = Handler()

        self.assertIsNone(handler.append(function_with_one_argument))

    def test_handler_rejects_function_without_arguments(self):
        handler = Handler()

        with self.assertRaises(AssertionError):
            handler.append(function_without_arguments)

    def test_handler_rejects_function_with_two_arguments(self):
        handler = Handler()

        with self.assertRaises(AssertionError):
            handler.append(function_with_two_arguments)

    def test_handler_calls_function_with_given_argument(self):
        handler = Handler()
        handler.append(function_with_one_argument)
        mock_handler_function = Mock()
        mock_handler_function.called_from_handler = False

        handler(mock_handler_function)

        self.assertTrue(mock_handler_function.called_from_handler)
