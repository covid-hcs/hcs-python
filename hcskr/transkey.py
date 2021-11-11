import re

import aiohttp

from . import crypto
from .keypad import KeyPad


class mTransKey:
    def __init__(self, servlet_url):
        self.servlet_url = servlet_url
        self.crypto = crypto.Crypto()
        self.token = ""
        self.initTime = ""
        self.decInitTime = ""
        self.qwerty = []
        self.number = []
        self.keyIndex = ""

    async def _get_data(self):
        async with aiohttp.ClientSession() as session:
            await self._get_token(session)
            await self._get_init_time(session)
            await self._get_public_key(session)
            await self._get_key_info(session)

    async def _get_token(self, session: aiohttp.ClientSession):
        async with session.get("{}?op=getToken".format(self.servlet_url)) as resp:
            txt = await resp.text()
            self.token = re.findall("var TK_requestToken=(.*);", txt)[0]

    async def _get_init_time(self, session: aiohttp.ClientSession):
        async with session.get("{}?op=getInitTime".format(self.servlet_url)) as resp:
            txt = await resp.text()
            self.initTime = re.findall("var initTime='(.*)';", txt)[0]

    async def _get_public_key(self, session: aiohttp.ClientSession):
        async with session.post(self.servlet_url, data={
                "op": "getPublicKey",
                "TK_requestToken": self.token
            }
        ) as resp:
            key = await resp.text()
            self.crypto.set_pub_key(key)

    async def _get_key_info(self, session: aiohttp.ClientSession):
        async with session.post(
            self.servlet_url,
            data={
                "op": "getKeyInfo",
                "key": self.crypto.get_encrypted_key(),
                "transkeyUuid": self.crypto.uuid,
                "useCert": "true",
                "TK_requestToken": self.token,
                "mode": "common",
            },
        ) as resp:
            key_data = await resp.text()
            qwerty, num = key_data.split("var number = new Array();")

            qwerty_keys = []
            number_keys = []

            for p in qwerty.split("qwertyMobile.push(key);")[:-1]:
                points = re.findall("key\.addPoint\((\d+), (\d+)\);", p)
                qwerty_keys.append(points[0])

            for p in num.split("number.push(key);")[:-1]:
                points = re.findall("key\.addPoint\((\d+), (\d+)\);", p)
                number_keys.append(points[0])

            self.qwerty = qwerty_keys
            self.number = number_keys

    async def new_keypad(self, key_type, name, inputName, fieldType="password"):
        await self._get_data()
        async with aiohttp.ClientSession() as session:
            key_index_res = await session.post(
                self.servlet_url,
                data={
                    "op": "getKeyIndex",
                    "name": "password",
                    "keyType": "single",
                    "keyboardType": "number",
                    "fieldType": "password",
                    "inputName": "password",
                    "parentKeyboard": "false",
                    "transkeyUuid": self.crypto.uuid,
                    "exE2E": "false",
                    "TK_requestToken": self.token,
                    "isCrt": "false",
                    "allocationIndex": "3011907012",
                    "keyIndex": "",
                    "initTime": self.initTime,
                    "talkBack": "true"
                }
            )
            self.keyIndex = await key_index_res.text()

            async with session.post(
                self.servlet_url,
                data={
                    "op": "getDummy",
                    "name": name,
                    "keyType": "single",
                    "keyboardType": "number",
                    "fieldType": fieldType,
                    "inputName": inputName,
                    "transkeyUuid": self.crypto.uuid,
                    "exE2E": "false",
                    "isCrt": "false",
                    "allocationIndex": "3011907012",
                    "keyIndex": self.keyIndex,
                    "initTime": self.initTime,
                    "TK_requestToken": self.token,
                    "dummy": "undefined",
                    "talkBack": "true",
                },
            ) as resp:
                skip_data = await resp.text()
                skip = skip_data.split(",")

                return KeyPad(self.crypto, key_type, skip, self.number, self.initTime)

    def hmac_digest(self, message):
        return self.crypto.hmac_digest(message)

    def get_uuid(self):
        return self.crypto.uuid
