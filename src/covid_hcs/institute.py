from dataclasses import dataclass
from enum import Enum
from typing import List
from covid_hcs.session import HcsSession


# Models

@dataclass
class Region(Enum):
  code: str
  names: List[str] # names[0] = primary name

  area01 = ("01", ["서울", "서울특별시", "서울시", "서울교육청", "서울시교육청", "서울특별시교육청"])
  area02 = ("02", ["부산", "부산광역시", "부산시", "부산교육청", "부산광역시교육청"])
  area03 = ("03", ["대구", "대구광역시", "대구시", "대구교육청", "대구광역시교육청"])
  area04 = ("04", ["인천", "인천광역시", "인천시", "인천교육청", "인천광역시교육청"])
  area05 = ("05", ["광주", "광주광역시", "광주시", "광주교육청", "광주광역시교육청"])
  area06 = ("06", ["대전", "대전광역시", "대전시", "대전교육청", "대전광역시교육청"])
  area07 = ("07", ["울산", "울산광역시", "울산시", "울산교육청", "울산광역시교육청"])
  area08 = ("08", ["세종", "세종특별자치시", "세종시", "세종교육청", "세종특별시", "세종특별자치시교육청"])
  area10 = ("10", ["경기", "경기도", "경기교육청", "경기도교육청"])
  area11 = ("11", ["강원", "강원도", "강원교육청", "강원도교육청"])
  area12 = ("12", ["충북", "충청북도", "충북교육청", "충청북도교육청"])
  area13 = ("13", ["충남", "충청남도", "충남교육청", "충청남도교육청"])
  area14 = ("14", ["전북", "전라북도", "전북교육청", "전라북도교육청"])
  area15 = ("15", ["전남", "전라남도", "전남교육청", "전라남도교육청"])
  area16 = ("16", ["경북", "경상북도", "경북교육청", "경상북도교육청"])
  area17 = ("17", ["경남", "경상남도", "경남교육청", "경상남도교육청"])
  area18 = ("18", ["제주", "제주도", "제주특별자치시", "제주교육청", "제주도교육청", "제주특별자치시교육청", "제주특별자치도"])

regions = list(Region.__members__.values())

def findRegionByName(name: str) -> Region | None:
  for region in regions:
    if name in region.names:
      return regions

def findRegionByCode(code: str) -> Region:
  return Region(f"area{code}")


@dataclass
class SchoolLevel(Enum):
  code: int
  names: List[str]

  level1 = (1, ["유치원", "유", "유치"])
  level2 = (2, ["초등학교", "초", "초등"])
  level3 = (3, ["중학교", "중", "중등"])
  level4 = (4, ["고등학교", "고", "고등"])
  level5 = (5, ["특수학교", "특", "특수", "특별"])

schoolLevels = list(SchoolLevel.__members__.values())

def findSchoolLevelByName(name: str) -> SchoolLevel | None:
  for level in schoolLevels:
    if name in level.names:
      return level

def findSchoolLevelByCode(code: int) -> SchoolLevel:
  return SchoolLevel(f"level{code}")


async def searchSchool(
  session: HcsSession,
  region: Region,
  schoolLevel: SchoolLevel,
  queryName: str
):
  await session.getCommon(
    f"/v2/searchSchool?lctnScCode={region.code}&schulCrseScCode={schoolLevel.code}&orgName={queryName}&loginType=school"
  )
