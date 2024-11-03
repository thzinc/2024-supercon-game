# Game for the 2024 Hackaday Supercon 8 badge

Competitive game to play online with others. Fire projectiles into the center and avoid projectiles fired at you!

## Quickstart

1. Copy the contents of [`badge`](./badge/) to the Pico.
2. Update [`constants.py`](./badge/constants.py) as is relevant
   - Set the `WIFI_SSID` and `WIFI_PASSWORD` to connect to your wifi network
   - (Optional) If you want to use a different MQTT broker, set `MQTT_HOST` as you see fit
   - Set the `GAME_ID` to something that you and your friends will use (play nice if you're using a public MQTT broker)
   - Set the `DEVICE_ID` to something unique to you (play nice if you're using a public MQTT broker)
3. Reset the badge
   - While booting, the center LED will be blue indicating it's trying to connect to wifi
   - When the game is about to start, the center LED will be green
   - Buttons
     - A - Move counter clockwise
     - B - Fire
     - C - Move clockwise
   - If you are hit by a projectile, press button B to resurrect yourself

## Building

## Code of Conduct

We are committed to fostering an open and welcoming environment. Please read our [code of conduct](CODE_OF_CONDUCT.md) before participating in or contributing to this project.

## Contributing

We welcome contributions and collaboration on this project. Please read our [contributor's guide](CONTRIBUTING.md) to understand how best to work with us.

## License and Authors

[![Daniel James logo](https://secure.gravatar.com/avatar/645145afc5c0bc24ba24c3d86228ad39?size=16) Daniel James](https://thzinc.com)

[![license](https://img.shields.io/github/license/thzinc/2024-supercon-iot-petal-matrix.svg)](https://github.com/thzinc/2024-supercon-iot-petal-matrix/blob/master/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/thzinc/2024-supercon-iot-petal-matrix.svg)](https://github.com/thzinc/2024-supercon-iot-petal-matrix/graphs/contributors)

This software is made available by Daniel James under the MIT license.
