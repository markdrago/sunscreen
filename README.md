# Sunscreen

Displays stats from an Enphase solar system.

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

## Hardware
This project uses a [Raspberry Pi Zero 2W](https://www.raspberrypi.com/products/raspberry-pi-zero-2-w/) and a [Waveshare 3.5 inch capacitive touchscreen](https://www.waveshare.com/3.5inch-dpi-lcd.htm) ([amazon](https://www.amazon.com/Waveshare-3-5inch-Capacitive-LCD-DPI/dp/B08TBF5PHH)). The software ultimately just draws on a full-screen window so other screens should work, but it does assume a 640x480 resolution. 

To connect the screen to the pi, I used a 2x20 pin header ([amazon](amazon.com/Frienda-Break-Away-Connector-Compatible-Raspberry/dp/B083DYVWDN)) that gets soldered to the pi. The pi zero 2w doesn't have these pins built-in, but using a larger pi with the pins should work and would avoid the soldering. The enclosure would also need to be modified to accommodate a different pi.

## Enclosure

The enclosure is 3d-printable in three parts which are [accessible on Printables](https://www.printables.com/model/1263887-raspberry-pi-zero-2w-screen-enclosure). The [design is available in OnShape](https://cad.onshape.com/documents/6b2e0a7a0c37ff4f52c9387f/w/1d550cc9ef7a5481deb5838a/e/ee4d8f82cb50f08f01f2823e). See the printables post for instructions and additional components that are necessary for assembly.

## Envoy API Documentation

* [Matthew1471's Enphase-API Doc](https://github.com/Matthew1471/Enphase-API)
* [Official Enphase API Doc (pdf)](https://enphase.com/download/accessing-iq-gateway-local-apis-or-local-ui-token-based-authentication)

