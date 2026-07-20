import json
from pathlib import Path

WG0_PATH = Path("/etc/wireguard/wg0.json")


class WGStorage:
    def __init__(self):
        if not WG0_PATH.exists():
            raise FileNotFoundError(f"{WG0_PATH} не найден.")

    def _load(self):
        with open(WG0_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_server(self):
        data = self._load()
        return data["server"]

    def get_client(self, client_id: str):
        data = self._load()

        client = data["clients"].get(client_id)

        if not client:
            raise Exception(f"Клиент {client_id} не найден.")

        return client