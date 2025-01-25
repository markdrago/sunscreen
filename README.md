# Sunscreen

Displays stats from an enphase solar system.

## Setup

1. Clone the repository
1. Install poetry version 2.0 or later: https://python-poetry.org/docs/
1. Run `poetry install` to install dependencies
  * You may need to run `poetry lock` if your available python version differs
    from what was recorded in the lock file.
1. Copy `sunscreen.cfg.example` to `sunscreen.cfg` and update with correct
    settings.
1. Run `poetry run sunscreen` to start sunscreen.

## Envoy Access Token
The access token must be retrieved from https://entrez.enphaseenergy.com/. You
will have to enter a few letters from the beginning of your system name in the
'Select System' box before it auto-completes. The system name can be found on
the 'Site Details' section of the Enphase mobile app.

Note that the Enphase documentation states that these tokens are valid for 1
year for system owners, so this will eventually need to be repeated.

## Envoy API Documentation

* [Matthew1471's Enphase-API Doc](https://github.com/Matthew1471/Enphase-API)
* [Official Enphase API Doc (pdf)](https://enphase.com/download/accessing-iq-gateway-local-apis-or-local-ui-token-based-authentication)

