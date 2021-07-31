"""/config/custom_components/cryptoportfolio"""

"""Support for Etherscan sensors."""
from datetime import timedelta
import requests

# import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from constants import CONF_ADDRESS, CONF_NAME, CONF_TOKEN, CONF_TOKEN_ADDRESS, CONF_EXPLORER_API_URL, CONF_MAIN_COIN, \
    CONF_EXPLORER_API_KEY
from homeassistant.const import ATTR_ATTRIBUTION
import homeassistant.helpers.config_validation as cv

ATTRIBUTION = "Data provided by blockchain explorers"

SCAN_INTERVAL = timedelta(minutes=5)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ADDRESS): cv.string,
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_TOKEN): cv.string,
        vol.Optional(CONF_TOKEN_ADDRESS): cv.string,
        vol.Optional(CONF_EXPLORER_API_URL, default="https://api.etherscan.io/api"): cv.string,
        vol.Optional(CONF_MAIN_COIN, default="ETH"): cv.string,
        vol.Optional(CONF_EXPLORER_API_KEY): cv.string,
    }
)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the cryptoPortfolio sensors."""
    address = config.get(CONF_ADDRESS)
    explorer_api_url = config.get(CONF_EXPLORER_API_URL)
    main_coin = config.get(CONF_MAIN_COIN)
    explorer_api_key = config.get(CONF_EXPLORER_API_KEY)
    name = config.get(CONF_NAME)
    token = config.get(CONF_TOKEN)
    token_address = config.get(CONF_TOKEN_ADDRESS)

    if not explorer_api_url or not main_coin:
        """Default blockchain"""
        explorer_api_url = "https://api.etherscan.io/api"
        main_coin = "ETH"

    main_coin = main_coin.upper()

    if token:
        token = token.upper()
        if not name:
            name = f"{token} Balance"
    if not name:
        name = f"{main_coin} Balance"

    add_entities([CryptoPortfolioSensor(main_coin, explorer_api_url, explorer_api_key, name, address, token, token_address)], True)


class CryptoPortfolioSensor(SensorEntity):
    """Representation of an CryptoPortfolio sensor."""

    def __init__(self, main_coin, explorer_api_url, explorer_api_key, name, address, token, token_address):
        """Initialize the sensor."""
        self._main_coin = main_coin
        self._explorer_api_url = explorer_api_url
        self._explorer_api_key = explorer_api_key
        self._name = name
        self._address = address
        self._token_address = token_address
        self._token = token
        self._state = None
        self._unit_of_measurement = self._token or main_coin

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
        return data['result']

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
