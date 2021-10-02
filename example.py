import logging

from pirssi.connection import Connection
from pirssi.publisher import Publisher

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S%z",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    publisher = Publisher(Connection())
    publisher.connect()

    publisher.publish("I am alive")

    publisher.close()
