from pathlib import Path

from config.config import (
    WG_API_URL,
    WG_PASSWORD,
)
from vpn.api import WGEasyAPI


class VPNManager:
    def __init__(self):
        self.api = WGEasyAPI(
            WG_API_URL,
            WG_PASSWORD,
        )

    # ---------- Клиенты ----------

    def create_client(self, name: str) -> dict:
        self.api.post(
            "/api/wireguard/client",
            {"name": name},
        )

        clients = self.api.get("/api/wireguard/client")

        for client in clients:
            if client["name"] == name:
                return client

        raise Exception("Клиент не найден.")

    def create_client_bundle(self, client_name: str) -> dict:
        client = self.create_client(client_name)

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        config_path = temp_dir / f"{client['id']}.conf"

        config = self.api.download_config(client["id"])
        config_path.write_text(config, encoding="utf-8")

        return {
            "client": client,
            "config": config_path,
        }

    def delete_client(self, client_id: str):
        self.api.delete(
            f"/api/wireguard/client/{client_id}"
        )

    def enable_client(self, client_id: str):
        self.api.post(
            f"/api/wireguard/client/{client_id}/enable"
        )

    def disable_client(self, client_id: str):
        self.api.post(
            f"/api/wireguard/client/{client_id}/disable"
        )

    def get_clients(self):
        return self.api.get(
            "/api/wireguard/client"
        )

    def get_client(self, client_id: str):
        clients = self.get_clients()

        for client in clients:
            if client["id"] == client_id:
                return client

        return None