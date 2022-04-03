import re

from aiohttp import ClientSession

from . import crypto
from .keypad import KeyPad


class TransKey:
    def __init__(self, servlet_url: str):
        self.servlet_url = servlet_url
        self.crypto = crypto.Crypto()
        self.token = ""
        self.init_time = ""
        self.dec_init_time = ""
        self.qwerty = []
        self.number = []
        self.key_index = ""

    async def _get_data(self):
        async with ClientSession() as session:
            await self._get_token(session)
            await self._get_init_time(session)
            await self._get_public_key(session)
            await self._get_key_info(session)

    async def _get_token(self, session: ClientSession):
        async with session.get(f"{self.servlet_url}?op=getToken") as resp:
            txt = await resp.text()
            self.token = re.findall("var TK_requestToken=(.*);", txt)[0]

    async def _get_init_time(self, session: ClientSession):
        async with session.get(f"{self.servlet_url}?op=getInitTime") as resp:
            txt = await resp.text()
            self.init_time = re.findall("var initTime='(.*)';", txt)[0]

    async def _get_public_key(self, session: ClientSession):
        async with session.post(
            self.servlet_url, data={"op": "getPublicKey", "TK_requestToken": self.token}
        ) as resp:
            key = await resp.text()
            self.crypto.set_public_key(key)

    async def _get_key_info(self, session: ClientSession):
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

            for points_str in qwerty.split("qwertyMobile.push(key);")[:-1]:
                points = re.findall(r"key\.addPoint\((\d+), (\d+)\);", points_str)
                qwerty_keys.append(points[0])

            for points_str in num.split("number.push(key);")[:-1]:
                points = re.findall(r"key\.addPoint\((\d+), (\d+)\);", points_str)
                number_keys.append(points[0])

            self.qwerty = qwerty_keys
            self.number = number_keys

    async def new_keypad(self, key_type, name, input_name, field_type="password"):
        await self._get_data()
        async with ClientSession() as session:
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
                    "initTime": self.init_time,
                    "talkBack": "true",
                },
            )
            self.key_index = await key_index_res.text()

            async with session.post(
                self.servlet_url,
                data={
                    "op": "getDummy",
                    "name": name,
                    "keyType": "single",
                    "keyboardType": "number",
                    "fieldType": field_type,
                    "inputName": input_name,
                    "transkeyUuid": self.crypto.uuid,
                    "exE2E": "false",
                    "isCrt": "false",
                    "allocationIndex": "3011907012",
                    "keyIndex": self.key_index,
                    "initTime": self.init_time,
                    "TK_requestToken": self.token,
                    "dummy": "undefined",
                    "talkBack": "true",
                },
            ) as resp:
                skip_data = await resp.text()
                skip = skip_data.split(",")

                return KeyPad(self.crypto, key_type, skip, self.number, self.init_time)

    def hmac_digest(self, message):
        return self.crypto.hmac_digest(message)

    def get_uuid(self):
        return self.crypto.uuid
