import logging
import queue
import threading

_LOGGER = logging.getLogger(__name__)

# https://blockchain.info/api/q
# The API requests: Please limit your queries to a maximum of 1 every 10 seconds
# Aim for up to one call every 15 seconds to be safe
RATE_LIMIT = 15

class BlockChainInfoQueue():
    def __init__(self):
        self._queue = queue.Queue()        

        # check for new work every RATE_LIMIT seconds
        threading.Timer(RATE_LIMIT, self.processQueue).start()

    def addRequest(self, sensor):
        _LOGGER.debug(f"Queueing an update for {sensor.name}")
        self._queue.put(sensor)

    def processQueue(self):
        _LOGGER.debug(f"Checking queue: {self._queue.qsize()} entries")

        threading.Timer(RATE_LIMIT, self.processQueue).start()

        if self._queue.empty():
            return

        task = self._queue.get()
        task.execute()