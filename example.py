import argparse
import logging
from time import sleep

from pirssi.connection import Connection
from pirssi.consumer import Consumer
from pirssi.publisher import Publisher

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S%z",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(
    description="Example for running Pirssi publisher or consumer."
)
parser.add_argument("action", choices=["publisher", "consumer"])
arguments = parser.parse_args()


def run_example_publisher():
    publisher = Publisher(Connection())
    publisher.connect()

    messages_to_publish = [
        "I command you to do something",
        "I would like to query some information",
        "Something weird happened and you should know about it"
    ]

    for message in messages_to_publish:
        publisher.publish(message)
        sleep(1)

    publisher.close()


def example_handler(message):
    print(f"I just handled a message: {message}")


def run_example_consumer():
    consumer = Consumer(Connection())
    consumer.connect()

    consumer.add_handler(example_handler)

    try:
        while True:
            consumer.read_messages()
            sleep(1)
    except KeyboardInterrupt:
        consumer.close()


if __name__ == '__main__':
    if arguments.action == "publisher":
        run_example_publisher()
    elif arguments.action == "consumer":
        run_example_consumer()
