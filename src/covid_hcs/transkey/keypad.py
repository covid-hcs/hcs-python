from random import randint

from covid_hcs.transkey.crypto import Crypto


class KeyPad:
    def __init__(self, crypto: Crypto, keyType, skipData, keys, initTime):
        if keyType != "number":
            raise Exception("Only Number")

        self.crypto = crypto
        self.keyType = keyType
        self.skipData = skipData
        self.keys = keys
        self.initTime = initTime

    def getGeo(self, message):
        geos = []
        for val in list(message):
            if val.isnumeric():
                geos.append(self.keys[self.skipData.index(val)])
            else:
                raise Exception("Only Number")
        return geos

    def geosEncrypt(self, geos):
        iv = bytes(
            [
                0x4D,
                0x6F,
                0x62,
                0x69,
                0x6C,
                0x65,
                0x54,
                0x72,
                0x61,
                0x6E,
                0x73,
                0x4B,
                0x65,
                0x79,
                0x31,
                0x30,
            ]
        )
        out = ""

        for geo in geos:
            x, y = geo

            xbytes = bytes(map(int, list(x)))
            ybytes = bytes(map(int, list(y)))

            data = b"%b %b %b %%b" % (xbytes, ybytes, self._timeToBytes())
            data += self._randomBytes(48 - len(data))
            out += "$" + self.crypto.seed_encrypt(iv, data).hex(",")
        return out

    def encryptPassword(self, pw):
        geos = self.getGeo(pw)
        return self.geosEncrypt(geos)

    def _randomBytes(self, length):
        out = []
        for _ in range(length):
            out.append(randint(0, 100))
        return bytes(out)

    def _timeToBytes(self):
        out = []
        for char in self.initTime:
            if char.isalpha():
                out.append(ord(char))
            else:
                out.append(int(char))
        return bytes(out)
