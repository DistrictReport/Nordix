import requests

from config.config import WG_API_URL, WG_PASSWORD


class WGEasyAPI:
    def __init__(self, host: str = WG_API_URL, password: str = WG_PASSWORD):
        self.host = host.rstrip("/")
        self.password = password

        self.session = requests.Session()

        # Полностью отключаем использование любых прокси
        self.session.trust_env = False
        self.session.proxies = {}

        self.login()

    def login(self):
        response = self.session.post(
            f"{self.host}/api/session",
            json={"password": self.password},
            timeout=15,
            proxies={},
        )

        response.raise_for_status()

    def _request(self, method: str, endpoint: str, **kwargs):
        response = self.session.request(
            method,
            f"{self.host}{endpoint}",
            timeout=15,
            proxies={},
            **kwargs,
        )

        if response.status_code == 401:
            self.login()

            response = self.session.request(
                method,
                f"{self.host}{endpoint}",
                timeout=15,
                proxies={},
                **kwargs,
            )

        response.raise_for_status()
        return response

    def get(self, endpoint: str):
        response = self._request("GET", endpoint)

        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()

        return response.text

    def post(self, endpoint: str, data: dict | None = None):
        response = self._request(
            "POST",
            endpoint,
            json=data,
        )

        if not response.text:
            return True

        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()

        return response.text

    def delete(self, endpoint: str):
        response = self._request(
            "DELETE",
            endpoint,
        )

        if not response.text:
            return True

        if "application/json" in response.headers.get("Content-Type", ""):
            return response.json()

        return response.text

    def download_config(self, client_id: str):
        return self._request(
            "GET",
            f"/api/wireguard/client/{client_id}/configuration",
        ).text

    def download_qr(self, client_id: str):
        return self._request(
            "GET",
            f"/api/wireguard/client/{client_id}/qrcode.svg",
        ).content