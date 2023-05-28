import json
import time

from websockets import server
from asus_api import AsusIp


class Websocket:
    def __init__(self):
        self.start_server = server.serve(self._handler, "", 5555)
        self.asus_api = AsusIp()

    async def _handler(self, websocket):
        while True:
            data = {
                "uptime": self.asus_api.get_uptime_secs(),
                "cpu": self.asus_api.get_cpu_usage(),
                "memory": self.asus_api.get_memory_usage(),
                "traffic": self.asus_api.get_traffic(),
                "clients": self.asus_api.get_clients_info(),
            }

            await websocket.send(json.dumps(data))

            time.sleep(10)
