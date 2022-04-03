from dataclasses import dataclass
from enum import Enum
from covid_hcs.institute import Institute, SearchKey
from covid_hcs.session import HcsSession
from covid_hcs.utils import yes_no_to_bool


class LoginType(Enum):
    SCHOOL = "school"
    UNIVERSITY = "univ"
    OFFICE = "office"


@dataclass
class UsersIdToken:
    token: str


@dataclass
class UsersIdentifier:
    main_user_name: str
    agreement: bool

    token: UsersIdToken


async def find_user(
    session: HcsSession,
    institute: Institute,
    name: str,
    birthday: str,
    search_key: SearchKey,
    login_type: LoginType = LoginType.SCHOOL,
) -> UsersIdentifier:
    result = await session.post(
        "/v2/findUser",
        headers={"Content-Type": "application/json"},
        json={
            "orgCode": institute.code,
            "name": name,
            "birthday": birthday,
            "loginType": login_type.value,
            "searchKey": search_key.token,
            "stdntPNo": None,
        },
    )

    return UsersIdentifier(
        main_user_name=result["userName"],
        agreement=yes_no_to_bool(result["pInfAgrmYn"]),
        token=UsersIdToken(result["token"]),
    )
