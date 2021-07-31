
CONF_ADDRESS = "address"
CONF_NAME = "name"
CONF_TOKEN = "token"
CONF_TOKEN_ADDRESS = "token_address"
CONF_MAIN_COIN = "main_coin"
CONF_EXPLORER_API_URL = "explorer_api_url"
CONF_EXPLORER_API_KEY = "explorer_api_key"
CONF_DECIMALS = "decimals"

"""Used to fetch data from other blockchains which are not directly based on ETH (e.g. BSC) such as BTC, ..
It is assumed that you want to fetch from an ETH fork by default."""
CONF_BLOCKCHAIN = "blockchain"

SUPPORTED_BLOCKCHAIN_ETHORFORK = "ETH_OR_FORK"
SUPPORTED_BLOCKCHAIN_BTC = "BTC"
SUPPORTED_BLOCKCHAINS = [SUPPORTED_BLOCKCHAIN_ETHORFORK, SUPPORTED_BLOCKCHAIN_BTC]
