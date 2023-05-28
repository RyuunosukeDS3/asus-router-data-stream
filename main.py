from config import Config
from asus_api import AsusIp
from websocket import Websocket

import asyncio
import logging

config = Config()
websocket = Websocket()

config.logging_config()


async def main():
    async with websocket.start_server:
        await asyncio.Future()


asyncio.get_event_loop().run_until_complete(main())
