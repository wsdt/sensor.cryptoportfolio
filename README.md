# // Crypto Portfolio [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://bitbucket.org/lbesson/ansi-colors) [![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/github/license/wsdt/sensor.cryptoportfolio.svg)](https://github.com/wsdt/sensor.cryptoportfolio/blob/master/LICENSE) [![Donate](https://img.shields.io/badge/Donate-Pay%20me%20a%20coffee-3cf)](https://github.com/wsdt/Global/wiki/Donation) [![saythanks](https://img.shields.io/badge/say-thanks-ff69b4.svg)](https://saythanks.io/to/kevin.riedl.privat%40gmail.com)
Install this Hassio integration via HACS.


## Params
Add this to your `configuration.yaml`.

### Configuration for Ethereum or Ethereum forks such as Binance Smart Chain, ..

- address __required__
- name
- token
- token_address (if not provided, then main coin is used, e.g. ETH, BNB)
- explorer_api_key
- main_coin (default: `ETH`)
- explorer_api_url (default: `https://api.etherscan.io/api`)
- decimals (default: `18`)
- blockchain (default: `ETH_OR_FORK`)

---

### Configuration for BTC.

- address __required__
- name
- blockchain: "BTC"
(rest of the parameters is ignored)

---

## Examples

```
sensor:
  - platform: cryptoportfolio
    address: "...."
    token_address: "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
    token: "USDC"
    decimals: 6
    explorer_api_key: "...."
    
  - platform: cryptoportfolio
    address: "...."
    explorer_api_key: "...."
```

