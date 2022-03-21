import asyncio
import json
import sys
from base64 import b64decode, b64encode
from enum import Enum

import aiohttp
import jwt

from .mapping import encrypt, pubkey, schoolinfo
from .request import getClientVersion, search_school, send_hcsreq
from .transkey import mTransKey


class QuickTestResult(Enum):
    none = None
    negative = "0"
    positive = "1"


def selfcheck(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    customloginname: str = None,
    quicktestresult: QuickTestResult = QuickTestResult.negative,
    loop=asyncio.get_event_loop(),
):
    return loop.run_until_complete(
        asyncSelfCheck(name, birth, area, schoolname, level, password, customloginname, quicktestresult)
    )


def changePassword(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    newpassword: str,
    loop=asyncio.get_event_loop(),
):
    return loop.run_until_complete(
        asyncChangePassword(name, birth, area, schoolname, level, password, newpassword)
    )


def userlogin(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    loop=asyncio.get_event_loop(),
):
    return loop.run_until_complete(
        asyncUserLogin(
            name, birth, area, schoolname, level, password, aiohttp.ClientSession()
        )
    )


def generatetoken(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    loop=asyncio.get_event_loop(),
):
    return loop.run_until_complete(
        asyncGenerateToken(name, birth, area, schoolname, level, password)
    )


def tokenselfcheck(token: str, loop=asyncio.get_event_loop()):
    return loop.run_until_complete(asyncTokenSelfCheck(token))


async def asyncSelfCheck(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    customloginname: str = None,
    quicktestresult: QuickTestResult = QuickTestResult.negative
):
    async with aiohttp.ClientSession() as session:
        if customloginname is None:
            customloginname = name

        login_result = await asyncUserLogin(
            name, birth, area, schoolname, level, password, session
        )

        if login_result["error"]:
            return login_result

        try:
            res = await send_hcsreq(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": login_result["token"],
                },
                endpoint="/v2/selectUserGroup",
                school=login_result["info"]["schoolurl"],
                json={},
                session=session,
            )
            userdataobject = {}
            for user in res:
                if user["otherYn"] == "N":
                    userdataobject = user
                    break

            userPNo = userdataobject["userPNo"]
            token = userdataobject["token"]

            res = await send_hcsreq(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": token,
                },
                endpoint="/v2/getUserInfo",
                school=login_result["info"]["schoolurl"],
                json={"orgCode": login_result["schoolcode"], userPNo: userPNo},
                session=session,
            )

            token = res["token"]

        except Exception as e:
            return {
                "error": True,
                "code": "UNKNOWN",
                "message": "getUserInfo: 알 수 없는 에러 발생.",
                "detail": e
            }

        try:
            payload = {
                "rspns01": "1",
                "rspns02": "1",
                # "rspns08": "0",
                # "rspns09": "0",
                "rspns00": "Y",
                "upperToken": token,
                "upperUserNameEncpt": customloginname,
                "clientVersion": getClientVersion()
            }
            if quicktestresult == QuickTestResult.none:
                payload["rspns03"] = "1"
            else:
                payload["rspns03"] = None
            payload["rspns07"] = quicktestresult.value
            res = await send_hcsreq(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": token,
                },
                endpoint="/registerServey",
                school=login_result["info"]["schoolurl"],
                json=payload,
                session=session,
            )

            return {
                "error": False,
                "code": "SUCCESS",
                "message": "성공적으로 자가진단을 수행하였습니다.",
                "regtime": res["registerDtm"],
            }

        except Exception as e:
            return {"error": True, "code": "UNKNOWN", "message": "알 수 없는 에러 발생.", "detail": e}


async def asyncChangePassword(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    newpassword: str,
):
    async with aiohttp.ClientSession() as session:
        login_result = await asyncUserLogin(
            name, birth, area, schoolname, level, password, session
        )

        if login_result["error"]:
            return login_result

        try:
            res = await send_hcsreq(
                headers={
                    "Content-Type": "application/json",
                    "Authorization": login_result["token"],
                },
                endpoint="/v2/changePassword",
                school=login_result["info"]["schoolurl"],
                json={
                    "password": encrypt(password),
                    "newPassword": encrypt(newpassword),
                },
                session=session,
            )

            if res:
                return {
                    "error": False,
                    "code": "SUCCESS",
                    "message": "성공적으로 비밀번호 변경에 성공하였습니다.",
                }

        except Exception as e:
            return {
                "error": True,
                "code": "INCORRECTPASSWORD",
                "message": "getUserInfo: 알 수 없는 에러 발생.",
                "detail": e
            }


async def asyncUserLogin(
    name: str,
    birth: str,
    area: str,
    schoolname: str,
    level: str,
    password: str,
    session: aiohttp.ClientSession,
):
    name = encrypt(name)  # Encrypt Name
    birth = encrypt(birth)  # Encrypt Birth

    try:
        info = schoolinfo(area, level)  # Get schoolInfo from Hcs API

    except Exception as e:
        return {"error": True, "code": "FORMET", "message": "지역명이나 학교급을 잘못 입력하였습니다.", "detail": e}

    school_infos = await search_school(
        code=info["schoolcode"], level=info["schoollevel"], org=schoolname
    )
    
    token = school_infos["key"]

    if len(school_infos["schulList"]) > 5:
        return {
            "error": True,
            "code": "NOSCHOOL",
            "message": "너무 많은 학교가 검색되었습니다. 지역, 학교급을 제대로 입력하고 학교 이름을 보다 상세하게 적어주세요.",
            "detail": None
        }

    try:
        schoolcode = school_infos["schulList"][0]["orgCode"]

    except Exception as e:
        return {
            "error": True,
            "code": "NOSCHOOL",
            "message": "검색 가능한 학교가 없습니다. 지역, 학교급을 제대로 입력하였는지 확인해주세요.",
            "detail": e
        }

    try:
        res = await send_hcsreq(
            headers={"Content-Type": "application/json"},
            endpoint="/v2/findUser",
            school=info["schoolurl"],
            json={
                "orgCode": schoolcode,
                "name": name,
                "birthday": birth,
                "loginType": "school",
                "searchKey": token,
                "stdntPNo": None,
            },
            session=session,
        )

        token = res["token"]

    except Exception as e:
        return {
            "error": True,
            "code": "NOSTUDENT",
            "message": "학교는 검색하였으나, 입력한 정보의 학생을 찾을 수 없습니다.",
            "detail": e
        }

    try:
        mtk = mTransKey("https://hcs.eduro.go.kr/transkeyServlet")
        pw_pad = await mtk.new_keypad("number", "password", "password", "password")
        encrypted = pw_pad.encrypt_password(password)
        hm = mtk.hmac_digest(encrypted.encode())

        res = await send_hcsreq(
            headers={
                "Referer": "https://hcs.eduro.go.kr/",
                "Authorization": token,
                "X-Requested-With": "XMLHttpRequest",
                "Content-Type": "application/json;charset=utf-8",
            },
            endpoint="/v2/validatePassword",
            school=info["schoolurl"],
            json={
                "password": json.dumps(
                    {
                        "raon": [
                            {
                                "id": "password",
                                "enc": encrypted,
                                "hmac": hm,
                                "keyboardType": "number",
                                "keyIndex": mtk.keyIndex,
                                "fieldType": "password",
                                "seedKey": mtk.crypto.get_encrypted_key(),
                                "initTime": mtk.initTime,
                                "ExE2E": "false",
                            }
                        ]
                    }
                ),
                "deviceUuid": "",
                "makeSession": True,
            },
            session=session,
        )

        if "isError" in res:
            return {
                "error": True,
                "code": "PASSWORD",
                "message": "학생정보는 검색하였으나, 비밀번호가 틀립니다.",
            }

        token = res["token"]

    except Exception as e:
        return {
            "error": True,
            "code": "UNKNOWN",
            "message": f"validatePassword: 알 수 없는 에러 발생.",
            "detail": e
        }

    try:
        caller_name = str(sys._getframe(1).f_code.co_name)

    except Exception:
        caller_name = None

    if caller_name == "asyncSelfCheck" or caller_name == "asyncChangePassword":
        return {
            "error": False,
            "code": "SUCCESS",
            "message": "유저 로그인 성공!",
            "token": token,
            "info": info,
            "schoolcode": schoolcode,
        }

    return {"error": False, "code": "SUCCESS", "message": "유저 로그인 성공!"}


async def asyncGenerateToken(
    name: str, birth: str, area: str, schoolname: str, level: str, password: str
):
    async with aiohttp.ClientSession() as session:
        login_result = await asyncUserLogin(**locals())

        if login_result["error"]:
            return login_result

        data = {
            "name": str(name),
            "birth": str(birth),
            "area": str(area),
            "schoolname": str(schoolname),
            "level": str(level),
            "password": str(password),
        }

        jwt_token = jwt.encode(data, pubkey, algorithm="HS256")

        if isinstance(jwt_token, str):
            jwt_token = jwt_token.encode("utf8")

        token = b64encode(jwt_token).decode("utf8")

        return {
            "error": False,
            "code": "SUCCESS",
            "message": "자가진단 토큰 발급 성공!",
            "token": token,
        }


async def asyncTokenSelfCheck(token: str, customloginname: str = None):
    try:
        data = jwt.decode(b64decode(token), pubkey, algorithms="HS256")

    except Exception as e:
        return {"error": True, "code": "WRONGTOKEN", "message": "올바르지 않은 토큰입니다.", "detail": e}

    return await asyncSelfCheck(
        data["name"],
        data["birth"],
        data["area"],
        data["schoolname"],
        data["level"],
        data["password"],
        customloginname,
    )
