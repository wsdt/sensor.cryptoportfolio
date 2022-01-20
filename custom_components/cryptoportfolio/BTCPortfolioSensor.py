import requests
import logging

from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.components.sensor import SensorEntity

ATTRIBUTION = "Data provided by blockchain.info"

_LOGGER = logging.getLogger(__name__)

class BTCPortfolioSensor(SensorEntity):
    """Representation of an CryptoPortfolio sensor."""

    def __init__(self, name, address, queue):
        """Initialize the sensor."""
        self._name = name
        self._address = address
        self._queue = queue
        self._decimals = 8
        self._state = None
        self._unit_of_measurement = "BTC"

    @property
    def decimals(self):
        return self._decimals

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement this sensor expresses itself in."""
        return self._unit_of_measurement

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sensor."""
        return {ATTR_ATTRIBUTION: ATTRIBUTION}

    def update(self):
        """Queues a request to update the latest state of the sensor."""
        self._queue.addRequest(self)

    def execute(self):
        """Get the latest state of the sensor."""
        _LOGGER.debug(f"Getting BTC balance for {self._address}")

        r = requests.get(url=f"https://blockchain.info/q/addressbalance/{self._address}")

        if r.status_code == 429:
            _LOGGER.warning(f"blockchain.info is reporting a 429 Too Many Requests response")
            return

        data = r.json()
        self._state = int(data) / (10 ** self._decimals)
