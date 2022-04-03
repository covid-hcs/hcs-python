from typing import Optional
from aiohttp import ClientSession, ServerDisconnectedError

from covid_hcs.institute import Institute


class BaseHcsSession:
    client_version: str
    http: ClientSession

    def __init__(self, http: ClientSession = ClientSession()):
        self.http = http

    async def request(
        self,
        method: str,
        url: str,
        headers: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        error = None

        for _attempt in range(5):
            try:
                async with self.http.request(
                    method=method, url=url, json=json, headers=headers
                ) as response:
                    client_version = response.headers.get("X-Client-Version")
                    if client_version is not None:
                        self.client_version = client_version

                    return await response.json()

            except ServerDisconnectedError as e:
                error = e

        raise error


class HcsSession(BaseHcsSession):
    request_url_body: str

    def __init__(self, request_url_body: str, http: ClientSession = ClientSession()):
        super().__init__(http=http)
        self.request_url_body = request_url_body

    async def post(self, endpoint: str, headers: dict, json: dict):
        return await self.request(
            "GET",
            f"https://{self.request_url_body}{endpoint}",
            headers=headers,
            json=json,
        )


class CommonHcsSession(BaseHcsSession):
    async def get_common(self, endpoint: str, headers: Optional[dict] = None) -> dict:
        return await self.request(
            "GET", f"https://hcs.eduro.go.kr{endpoint}", headers=headers
        )

    def create_session(self, institute: Institute) -> HcsSession:
        return HcsSession(request_url_body=institute.request_url_body, http=self.http)
