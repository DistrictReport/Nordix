from pathlib import Path

import qrcode

from config.config import (
    WG_DNS,
    WG_HOST,
    WG_PORT,
    WG_ALLOWED_IPS,
    WG_MTU,
    WG_PERSISTENT_KEEPALIVE,
)
from vpn.api import WGEasyAPI
from vpn.storage import WGStorage


class VPNManager:
    def __init__(self):
        self.api = WGEasyAPI()
        self.storage = WGStorage()

    # ---------- Клиенты ----------

    def create_client(self, name: str) -> dict:
        self.api.post(
            "/api/wireguard/client",
            {"name": name}
        )

        clients = self.api.get("/api/wireguard/client")

        for client in clients:
            if client["name"] == name:
                return client

        raise Exception("Клиент не найден.")

    def create_client_bundle(self, client_name: str) -> dict:
        """
        Создает клиента WireGuard и сразу готовит
        конфигурационный файл и QR-код.
        """

        client = self.create_client(client_name)

        config_file = self.create_config_file(
            client["id"]
        )

        qr_file = self.generate_qr(
            client["id"]
        )

        return {
            "client": client,
            "config": config_file,
            "qr": qr_file
        }

    def delete_client(self, client_id: str):
        self.api.delete(f"/api/wireguard/client/{client_id}")

    def enable_client(self, client_id: str):
        self.api.post(f"/api/wireguard/client/{client_id}/enable")

    def disable_client(self, client_id: str):
        self.api.post(f"/api/wireguard/client/{client_id}/disable")

    # ---------- Получение данных ----------

    def get_client(self, client_id: str) -> dict:
        return self.storage.get_client(client_id)

    def get_server(self) -> dict:
        return self.storage.get_server()

    # ---------- WireGuard ----------

    def generate_config(self, client_id: str) -> str:
        server = self.get_server()
        client = self.get_client(client_id)

        return f"""[Interface]
PrivateKey = {client["privateKey"]}
Address = {client["address"]}/24
DNS = {WG_DNS}
MTU = {WG_MTU}

[Peer]
PublicKey = {server["publicKey"]}
PresharedKey = {client["preSharedKey"]}
AllowedIPs = {WG_ALLOWED_IPS}
Endpoint = {WG_HOST}:{WG_PORT}
PersistentKeepalive = {WG_PERSISTENT_KEEPALIVE}
"""

    def create_config_file(self, client_id: str) -> Path:
        config = self.generate_config(client_id)

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / f"{client_id}.conf"

        file_path.write_text(config, encoding="utf-8")

        return file_path

    def generate_qr(self, client_id: str) -> Path:
        config = self.generate_config(client_id)

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        qr.add_data(config)
        qr.make(fit=True)

        image = qr.make_image(
            fill_color="black",
            back_color="white",
        )

        temp_dir = Path("temp")
        temp_dir.mkdir(exist_ok=True)

        file_path = temp_dir / f"{client_id}.png"

        image.save(file_path)

        return file_path