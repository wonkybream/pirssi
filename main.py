import logging
from time import sleep

from pirssi.connection import Connection

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S%z",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    connection = Connection()
    connection.connect()
    sleep(5)
    connection.close()
