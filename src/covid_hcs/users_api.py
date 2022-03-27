from dataclasses import dataclass
from enum import Enum
from covid_hcs.institute import Institute, SearchKey
from covid_hcs.session import HcsSession
from covid_hcs.utils import yesNoToBool


class LoginType(Enum):
  school = 'school'
  university = 'univ'
  office = 'office'

@dataclass
class UsersIdToken:
  token: str

@dataclass
class UsersIdentifier:
  mainUserName: str
  agreement: bool

  token: UsersIdToken

async def findUser(
  session: HcsSession,
  institute: Institute,
  name: str,
  birthday: str,
  searchKey: SearchKey,
  loginType: LoginType = LoginType.school
) -> UsersIdentifier:
  result = await session.post(
    "/v2/findUser",
    headers={"Content-Type": "application/json"},
    json={
      "orgCode": institute.code,
      "name": name,
      "birthday": birthday,
      "loginType": loginType.value,
      "searchKey": searchKey.token,
      "stdntPNo": None,
    }
  )

  return UsersIdentifier(
    mainUserName=result["userName"],
    agreement=yesNoToBool(result["pInfAgrmYn"]),
    token=UsersIdToken(result["token"])
  )
