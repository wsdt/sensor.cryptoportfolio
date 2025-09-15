"""/config/custom_components/cryptoportfolio"""

"""Support for Etherscan sensors."""
from datetime import timedelta
import logging

# import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from .constants import CONF_ADDRESS, CONF_NAME, CONF_TOKEN, CONF_TOKEN_ADDRESS, CONF_EXPLORER_API_URL, CONF_MAIN_COIN, \
    CONF_EXPLORER_API_KEY, CONF_DECIMALS, CONF_BLOCKCHAIN, SUPPORTED_BLOCKCHAINS, SUPPORTED_BLOCKCHAIN_ETHORFORK, SUPPORTED_BLOCKCHAIN_BTC
from .ETHorForkPortfolioSensor import ETHorForkPortfolioSensor
from .BTCPortfolioSensor import BTCPortfolioSensor
from .BlockChainInfoQueue import BlockChainInfoQueue

import homeassistant.helpers.config_validation as cv

SCAN_INTERVAL = timedelta(minutes=5)

_LOGGER = logging.getLogger(__name__)

blockChainInfoQueue = BlockChainInfoQueue()

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ADDRESS): cv.string,  # TODO: [cv.string] == Array
        vol.Optional(CONF_NAME): cv.string,
        vol.Optional(CONF_TOKEN): cv.string,
        vol.Optional(CONF_TOKEN_ADDRESS): cv.string,
        vol.Optional(CONF_EXPLORER_API_URL, default="https://api.etherscan.io/v2/api?chainid=1"): cv.string,
        vol.Optional(CONF_MAIN_COIN, default="ETH"): cv.string,
        vol.Optional(CONF_DECIMALS, default=18): cv.positive_int,
        vol.Optional(CONF_EXPLORER_API_KEY): cv.string,
        vol.Optional(CONF_BLOCKCHAIN, default=SUPPORTED_BLOCKCHAIN_ETHORFORK): cv.string,
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
    decimals = config.get(CONF_DECIMALS)
    blockchain = config.get(CONF_BLOCKCHAIN)

    if not blockchain:
        blockchain = SUPPORTED_BLOCKCHAIN_ETHORFORK

    if blockchain == SUPPORTED_BLOCKCHAIN_ETHORFORK:

        if not explorer_api_key:
            _LOGGER.error("No api key provided for ETH or fork.")
            return False

        if not explorer_api_url or not main_coin:
            """Default blockchain"""
            explorer_api_url = "https://api.etherscan.io/v2/api?chainid=1"
            main_coin = "ETH"

        main_coin = main_coin.upper()

        if token:
            token = token.upper()
            if not name:
                name = f"{token} Balance"
            if not decimals:
                decimals = 9  # default value for tokens
        elif not decimals:
            decimals = 18

        if not name:
            name = f"{main_coin} Balance"

        add_entities([ETHorForkPortfolioSensor(main_coin, explorer_api_url, explorer_api_key, name, address, token,
                                               token_address, decimals)], True)

    elif blockchain == SUPPORTED_BLOCKCHAIN_BTC:
        if not name:
            name = "BTC Balance"

        add_entities([BTCPortfolioSensor(name, address, blockChainInfoQueue)], True)


    else:
        _LOGGER.error(f"Unsupported blockchain provided: {blockchain}")
        return False

