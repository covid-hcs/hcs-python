from typing import Dict

import aiohttp
from aiohttp.client_exceptions import ServerDisconnectedError

clientVersion: str = None

def getClientVersion():
    return clientVersion


async def send_hcsreq(
    headers: Dict,
    endpoint: str,
    school: str,
    json: Dict,
    session: aiohttp.ClientSession
):
    global clientVersion

    for attempt in range(5):
        try:
            async with session.post(
                headers=headers,
                url=f"https://{school}hcs.eduro.go.kr{endpoint}",
                json=json,
            ) as resp:
                clientVersion = resp.headers["X-Client-Version"]
                return await resp.json()
        except ServerDisconnectedError as e:
            if attempt >= 4:
                raise e
            continue


async def search_school(code: str, level: str, org: str):
    for attempt in range(5):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    url=f"https://hcs.eduro.go.kr/v2/searchSchool?lctnScCode={code}&schulCrseScCode={level}&orgName={org}&loginType=school"
                ) as resp:
                    return await resp.json()
        except ServerDisconnectedError as e:
            if attempt >= 4:
                raise e
            continue
