from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA


publicKeyBase64 = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2"
    "+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr"
    "+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc"
    "+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM"
    "/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB== "
)

def encrypt(n: str) -> str:
  global cipher
  if not cipher:
    publicKeyBytes = b64decode(publicKeyBase64)
    publicKey = RSA.importKey(publicKeyBytes)
    cipher = PKCS1_v1_5.new(publicKey)
  
  msg = n.encode("utf-8")
  length = 245 # 256 - 11 # '..It can be of variable length, but not longer than the RSA modulus (in bytes) minus 11'

  dataList = [msg[i : i + length] for i in list(range(0, len(msg), length))]

  encryptedDataList = [
    b64encode(cipher.encrypt(message=data)) for data in dataList
  ]

  return "".join([data.decode("utf-8") for data in encryptedDataList])
