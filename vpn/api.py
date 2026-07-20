import requests

from config.config import WG_API_URL, WG_PASSWORD


class WGEasyAPI:
    def __init__(self):
        self.host = WG_API_URL.rstrip("/")
        self.password = WG_PASSWORD

        self.session = requests.Session()

        self.login()

    def login(self):
        response = self.session.post(
            f"{self.host}/api/session",
            json={
                "password": self.password
            },
            timeout=15
        )

        response.raise_for_status()

    def get(self, endpoint: str):
        response = self.session.get(
            f"{self.host}{endpoint}",
            timeout=15
        )

        if response.status_code == 401:
            self.login()

            response = self.session.get(
                f"{self.host}{endpoint}",
                timeout=15
            )

        response.raise_for_status()

        return response.json()

    def post(self, endpoint: str, data: dict | None = None):
        response = self.session.post(
            f"{self.host}{endpoint}",
            json=data,
            timeout=15
        )

        if response.status_code == 401:
            self.login()

            response = self.session.post(
                f"{self.host}{endpoint}",
                json=data,
                timeout=15
            )

        response.raise_for_status()

        if response.text:
            return response.json()

        return True

    def delete(self, endpoint: str):
        response = self.session.delete(
            f"{self.host}{endpoint}",
            timeout=15
        )

        if response.status_code == 401:
            self.login()

            response = self.session.delete(
                f"{self.host}{endpoint}",
                timeout=15
            )

        response.raise_for_status()

        if response.text:
            return response.json()

        return True