import requests
from homeassistant.const import ATTR_ATTRIBUTION
from homeassistant.components.sensor import SensorEntity

ATTRIBUTION = "Data provided by blockchain explorers"

class ETHorForkPortfolioSensor(SensorEntity):
    """Representation of an CryptoPortfolio sensor."""

    def __init__(self, main_coin, explorer_api_url, explorer_api_key, name, address, token, token_address, decimals):
        """Initialize the sensor."""
        self._main_coin = main_coin
        self._explorer_api_url = explorer_api_url
        self._explorer_api_key = explorer_api_key
        self._name = name
        self._address = address
        self._token_address = token_address
        self._decimals = decimals
        self._token = token
        self._state = None
        self._unit_of_measurement = self._token or main_coin

    @property
    def decimals(self):
        return self._decimals

    @property
    def main_coin(self):
        return self._main_coin

    @property
    def explorer_api_url(self):
        return self._explorer_api_url

    @property
    def explorer_api_key(self):
        return self._explorer_api_key

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

    def fetch_value(self, params):
        r = requests.get(url=self._explorer_api_url, params=params)
        data = r.json()
        return int(data['result']) / (10 ** self._decimals)

    def update(self):
        """Get the latest state of the sensor."""

        if self._token_address:
            self._state = self.fetch_value({'module': 'account', 'action': 'tokenbalance',
                                            'contractaddress': self._token_address, 'address': self._address,
                                            'tag': 'latest', 'apikey': self._explorer_api_key})
        else:
            self._state = self.fetch_value({'module': 'account', 'action': 'balance',
                                            'address': self._address, 'tag': 'latest',
                                            'apikey': self._explorer_api_key})
