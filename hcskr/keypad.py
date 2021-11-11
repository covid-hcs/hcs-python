from random import randint


class KeyPad:
    def __init__(self, crypto, key_type, skip_data, keys, initTime):
        if key_type != "number":
            raise Exception("Only Number")

        self.crypto = crypto
        self.key_type = key_type
        self.skip_data = skip_data
        self.keys = keys
        self.initTime = initTime

    def get_geo(self, message):
        geos = []
        for val in list(message):
            if val.isnumeric():
                geos.append(self.keys[self.skip_data.index(val)])
            else:
                raise Exception("Only Number")
        return geos

    def geos_encrypt(self, geos):
        iv = bytes([0x4d, 0x6f, 0x62, 0x69, 0x6c, 0x65, 0x54, 0x72, 0x61, 0x6e, 0x73, 0x4b, 0x65, 0x79, 0x31, 0x30])
        out = ""

        for geo in geos:
            x, y = geo
            
            xbytes = bytes(map(int, list(x)))
            ybytes = bytes(map(int, list(y)))
            
            data = b"%b %b %b %%b" % (xbytes, ybytes, self._time_to_bytes())
            data += self._randomBytes(48-len(data))
            out += "$"+self.crypto.seed_encrypt(iv, data).hex(",")
        return out

    def encrypt_password(self, pw):
        geos = self.get_geo(pw)
        return self.geos_encrypt(geos)

    def _randomBytes(self, length):
        out = []
        for _ in range(length):
            out.append(randint(0, 100))
        return bytes(out)
    
    def _time_to_bytes(self):
        out = []
        for char in self.initTime:
            if char.isalpha():
                out.append(ord(char))
            else:
                out.append(int(char))
        return bytes(out)
