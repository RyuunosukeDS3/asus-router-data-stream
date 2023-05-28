import logging
import json
import base64
import os
import time
import requests


class AsusIp:
    def __init__(self):
        self.asus_router_ip = os.getenv("ASUS_ROUTER_IP")
        self.headers = {
            "user-Agent": "asusrouter-Android-DUTUtil-1.0.0.245",
        }
        self.login()

    def login(self):
        username = os.getenv("ASUS_ROUTER_LOGIN")
        password = os.getenv("ASUS_ROUTER_PASSWORD")
        account = f"{username}:{password}"

        account_string_bytes = account.encode("ascii")
        account_base64_bytes = base64.b64encode(account_string_bytes)
        login = account_base64_bytes.decode("ascii")

        url = f"http://{self.asus_router_ip}/login.cgi"
        data = f"login_authorization={login}"

        response = requests.post(url=url, data=data, headers=self.headers, timeout=60)
        json_body = response.json()

        self.headers["cookie"] = f"asus_token={json_body['asus_token']}"

    def _get(self, command):
        data = f"hook={command}"
        try:
            response = requests.post(
                url=f"http://{self.asus_router_ip}/appGet.cgi",
                data=data,
                headers=self.headers,
                timeout=60,
            ).text
        except Exception as err:
            logging.error("Failed to get %s with error: %s", command, err)
        return response

    def get_uptime_secs(self):
        response = self._get("uptime()")
        since = response.partition(":")[2].partition("(")[0]
        uptime = response.partition("(")[2].partition(" ")[0]
        response = json.loads(
            "{" + f'"since":"{since}", "uptime":"{uptime}"' + "}"
        )
        return int(response["uptime"])

    def get_memory_usage(self):
        response = self._get("memory_usage()")
        return json.loads("{" + response[17:])

    def get_cpu_usage(self):
        response = self._get("cpu_usage()")
        return json.loads("{" + response[14:])

    def get_traffic(self):
        meas_1 = self._get("netdev(appobj)")
        time.sleep(2)
        meas_2 = self._get("netdev(appobj)")
        meas_1 = json.loads(meas_1)
        meas_2 = json.loads(meas_2)
        persec = {}
        upload = int(meas_2["netdev"]["INTERNET_tx"], base=16) * 8 / 1024 / 1024 / 2
        upload -= int(meas_1["netdev"]["INTERNET_tx"], base=16) * 8 / 1024 / 1024 / 2
        persec["upload"] = upload
        download = int(meas_2["netdev"]["INTERNET_rx"], base=16) * 8 / 1024 / 1024 / 2
        download -= int(meas_1["netdev"]["INTERNET_rx"], base=16) * 8 / 1024 / 1024 / 2
        persec["download"] = download
        return json.dumps({"speed": persec})

    def get_clients_info(self):
        clients = json.loads(self._get("get_clientlist()"))
        client_list = []
        for client in clients["get_clientlist"]:
            if (
                (len(client) == 17)
                and ("isOnline" in clients["get_clientlist"][client])
                and (clients["get_clientlist"][client]["isOnline"] == "1")
            ):
                client_list.append(
                    {
                        "name": clients["get_clientlist"][client]["name"],
                        "nickName": clients["get_clientlist"][client]["nickName"],
                        "ip": clients["get_clientlist"][client]["ip"],
                        "mac": clients["get_clientlist"][client]["mac"],
                        "isOnline": clients["get_clientlist"][client]["isOnline"],
                        "curTx": clients["get_clientlist"][client]["curTx"],
                        "curRx": clients["get_clientlist"][client]["curRx"],
                        "totalTx": clients["get_clientlist"][client]["totalTx"],
                        "totalRx": clients["get_clientlist"][client]["totalRx"],
                    }
                )
        return json.loads(json.dumps(client_list))
