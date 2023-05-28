import asyncio

from config import Config
from websocket import Websocket

config = Config()
websocket = Websocket()

config.logging_config()


async def main():
    async with websocket.start_server:
        await asyncio.Future()


asyncio.get_event_loop().run_until_complete(main())
