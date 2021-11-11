from base64 import b64decode, b64encode

from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

pubkey = (
    "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA81dCnCKt0NVH7j5Oh2"
    "+SGgEU0aqi5u6sYXemouJWXOlZO3jqDsHYM1qfEjVvCOmeoMNFXYSXdNhflU7mjWP8jWUmkYIQ8o3FGqMzsMTNxr"
    "+bAp0cULWu9eYmycjJwWIxxB7vUwvpEUNicgW7v5nCwmF5HS33Hmn7yDzcfjfBs99K5xJEppHG0qc"
    "+q3YXxxPpwZNIRFn0Wtxt0Muh1U8avvWyw03uQ/wMBnzhwUC8T4G5NclLEWzOQExbQ4oDlZBv8BM"
    "/WxxuOyu0I8bDUDdutJOfREYRZBlazFHvRKNNQQD2qDfjRz484uFs7b5nykjaMB9k/EJAuHjJzGs9MMMWtQIDAQAB== "
)

areas = {
    "area1": ["서울", "서울시", "서울교육청", "서울시교육청", "서울특별시", "서울특별시교육청"],
    "area2": ["부산", "부산광역시", "부산시", "부산교육청", "부산광역시교육청"],
    "area3": ["대구", "대구광역시", "대구시", "대구교육청", "대구광역시교육청"],
    "area4": ["인천", "인천광역시", "인천시", "인천교육청", "인천광역시교육청"],
    "area5": ["광주", "광주광역시", "광주시", "광주교육청", "광주광역시교육청"],
    "area6": ["대전", "대전광역시", "대전시", "대전교육청", "대전광역시교육청"],
    "area7": ["울산", "울산광역시", "울산시", "울산교육청", "울산광역시교육청"],
    "area8": ["세종", "세종특별시", "세종시", "세종교육청", "세종특별자치시", "세종특별자치시교육청"],
    "area10": ["경기", "경기도", "경기교육청", "경기도교육청"],
    "area11": ["강원", "강원도", "강원교육청", "강원도교육청"],
    "area12": ["충북", "충청북도", "충북교육청", "충청북도교육청"],
    "area13": ["충남", "충청남도", "충남교육청", "충청남도교육청"],
    "area14": ["전북", "전라북도", "전북교육청", "전라북도교육청"],
    "area15": ["전남", "전라남도", "전남교육청", "전라남도교육청"],
    "area16": ["경북", "경상북도", "경북교육청", "경상북도교육청"],
    "area17": ["경남", "경상남도", "경남교육청", "경상남도교육청"],
    "area18": ["제주", "제주도", "제주특별자치시", "제주교육청", "제주도교육청", "제주특별자치시교육청", "제주특별자치도"],
}
levels = {
    "level1": ["유치원", "유", "유치"],
    "level2": ["초등학교", "초", "초등"],
    "level3": ["중학교", "중", "중등"],
    "level4": ["고등학교", "고", "고등"],
    "level5": ["특수학교", "특", "특수", "특별"],
}


def encrypt(n):
    rsa_public_key = b64decode(pubkey)
    pub_key = RSA.importKey(rsa_public_key)
    cipher = Cipher_pkcs1_v1_5.new(pub_key)
    msg = n.encode("utf-8")
    length = 245

    msg_list = [msg[i : i + length] for i in list(range(0, len(msg), length))]

    encrypt_msg_list = [
        b64encode(cipher.encrypt(message=msg_str)) for msg_str in msg_list
    ]

    return encrypt_msg_list[0].decode("utf-8")


def schoolinfo(area, level):
    info = {}
    if area in areas["area1"]:
        schoolcode = "01"
        schoolurl = "sen"
    if area in areas["area2"]:
        schoolcode = "02"
        schoolurl = "pen"
    if area in areas["area3"]:
        schoolcode = "03"
        schoolurl = "dge"
    if area in areas["area4"]:
        schoolcode = "04"
        schoolurl = "ice"
    if area in areas["area5"]:
        schoolcode = "05"
        schoolurl = "gen"
    if area in areas["area6"]:
        schoolcode = "06"
        schoolurl = "dje"
    if area in areas["area7"]:
        schoolcode = "07"
        schoolurl = "use"
    if area in areas["area8"]:
        schoolcode = "08"
        schoolurl = "sje"
    if area in areas["area10"]:
        schoolcode = 10
        schoolurl = "goe"
    if area in areas["area11"]:
        schoolcode = 11
        schoolurl = "kwe"
    if area in areas["area12"]:
        schoolcode = 12
        schoolurl = "cbe"
    if area in areas["area13"]:
        schoolcode = 13
        schoolurl = "cne"
    if area in areas["area14"]:
        schoolcode = 14
        schoolurl = "jbe"
    if area in areas["area15"]:
        schoolcode = 15
        schoolurl = "jne"
    if area in areas["area16"]:
        schoolcode = 16
        schoolurl = "gbe"
    if area in areas["area17"]:
        schoolcode = 17
        schoolurl = "gne"
    if area in areas["area18"]:
        schoolcode = 18
        schoolurl = "jje"
    if level in levels["level1"]:
        schoollevel = 1
    if level in levels["level2"]:
        schoollevel = 2
    if level in levels["level3"]:
        schoollevel = 3
    if level in levels["level4"]:
        schoollevel = 4
    if level in levels["level5"]:
        schoollevel = 5
    info["schoolcode"] = schoolcode
    info["schoollevel"] = schoollevel
    info["schoolurl"] = schoolurl
    return info
