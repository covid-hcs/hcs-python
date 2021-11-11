import hashlib
import hmac
import os
from base64 import b64decode

from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA1
from Crypto.PublicKey import RSA

from . import seed


class Crypto:
    def __init__(self):
        self.uuid = os.urandom(int(32)).hex()
        self.genSessionKey = os.urandom(int(8)).hex()
        self.key = None
        self.sessionKey = [int(i, 16) for i in list(self.genSessionKey)]

    def _pad(self, txt):
        if len(txt) < 16:
            txt += b"\x00" * (16 - len(txt))
        return txt

    def rsa_encrypt(self, data):
        cipher = PKCS1_OAEP.new(key=self.key, hashAlgo=SHA1)
        return cipher.encrypt(data).hex()

    def get_encrypted_key(self):
        return self.rsa_encrypt(self.genSessionKey.encode())

    def hmac_digest(self, msg: bytes):
        return hmac.new(
            msg=msg, key=self.genSessionKey.encode(), digestmod=hashlib.sha256
        ).hexdigest()

    def seed_encrypt(self, iv, data):
        s = seed.SEED()
        round_key = s.SeedRoundKey(bytes(self.sessionKey))
        return s.my_cbc_encrypt(self._pad(data), round_key, iv)

    def set_pub_key(self, b64):
        data = b64decode(b64)
        self.key = RSA.import_key(data)
