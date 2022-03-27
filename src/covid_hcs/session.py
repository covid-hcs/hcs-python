from typing import Optional
from aiohttp import ClientSession, ServerDisconnectedError


class CommonHcsSession:
  clientVersion: str
  http: ClientSession

  def __init__(self):
      self.http = ClientSession()

  async def getCommon(self, endpoint: str, headers: dict = {}) -> dict:
    return await self.request(f"https://hcs.eduro.go.kr{endpoint}", headers=headers)

  async def request(
    self,
    method: str,
    url: str,
    headers: dict = {},
    json: Optional[dict] = None
  ) -> dict:
    error = None

    for attempt in range(5):
      try:
        async with self.http.request(
          method=method,
          url=url,
          json=json,
          headers=headers
        ) as response:
          clientVersion =  response.headers.get("X-Client-Version")
          if clientVersion != None:
            self.clientVersion = clientVersion
          
          return await response.json()
      
      except ServerDisconnectedError as e:
        error = e

    raise error


class HcsSession(CommonHcsSession):
  requestUrlBody: str

  def __init__(self, requestUrlBody: str):
    super().__init__()
    self.requestUrlBody = requestUrlBody
  
  async def post(self, endpoint: str, headers: dict, json: dict):
    return await self.request(f"https://{self.requestUrlBody}{endpoint}", headers=headers, json=json)

