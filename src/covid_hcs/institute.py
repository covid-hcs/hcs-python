from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List

from yarl import URL
from covid_hcs.session import CommonHcsSession

# Models


@dataclass
class Region(Enum):
    code: str
    names: List[str]  # names[0] = primary name

    AREA_01 = ("01", ["서울", "서울특별시", "서울시", "서울교육청", "서울시교육청", "서울특별시교육청"])
    AREA_02 = ("02", ["부산", "부산광역시", "부산시", "부산교육청", "부산광역시교육청"])
    AREA_03 = ("03", ["대구", "대구광역시", "대구시", "대구교육청", "대구광역시교육청"])
    AREA_04 = ("04", ["인천", "인천광역시", "인천시", "인천교육청", "인천광역시교육청"])
    AREA_05 = ("05", ["광주", "광주광역시", "광주시", "광주교육청", "광주광역시교육청"])
    AREA_06 = ("06", ["대전", "대전광역시", "대전시", "대전교육청", "대전광역시교육청"])
    AREA_07 = ("07", ["울산", "울산광역시", "울산시", "울산교육청", "울산광역시교육청"])
    AREA_08 = ("08", ["세종", "세종특별자치시", "세종시", "세종교육청", "세종특별시", "세종특별자치시교육청"])
    AREA_10 = ("10", ["경기", "경기도", "경기교육청", "경기도교육청"])
    AREA_11 = ("11", ["강원", "강원도", "강원교육청", "강원도교육청"])
    AREA_12 = ("12", ["충북", "충청북도", "충북교육청", "충청북도교육청"])
    AREA_13 = ("13", ["충남", "충청남도", "충남교육청", "충청남도교육청"])
    AREA_14 = ("14", ["전북", "전라북도", "전북교육청", "전라북도교육청"])
    AREA_15 = ("15", ["전남", "전라남도", "전남교육청", "전라남도교육청"])
    AREA_16 = ("16", ["경북", "경상북도", "경북교육청", "경상북도교육청"])
    AREA_17 = ("17", ["경남", "경상남도", "경남교육청", "경상남도교육청"])
    AREA_18 = (
        "18",
        ["제주", "제주도", "제주특별자치시", "제주교육청", "제주도교육청", "제주특별자치시교육청", "제주특별자치도"],
    )

    @staticmethod
    def find_by_name(name: str) -> Region | None:
        for region in Region.__members__.values():
            if name in region.names:
                return region

    @staticmethod
    def from_code(code: str) -> Region | None:
        for region in Region.__members__.values():
            if code == region.code:
                return region


@dataclass
class SchoolLevel(Enum):
    code: int
    names: List[str]

    LEVEL_1 = (1, ["유치원", "유", "유치"])
    LEVEL_2 = (2, ["초등학교", "초", "초등"])
    LEVEL_3 = (3, ["중학교", "중", "중등"])
    LEVEL_4 = (4, ["고등학교", "고", "고등"])
    LEVEL_5 = (5, ["특수학교", "특", "특수", "특별"])

    @staticmethod
    def find_by_name(name: str) -> SchoolLevel | None:
        for level in SchoolLevel.__members__.values():
            if name in level.names:
                return level

    @staticmethod
    def from_code(code: int) -> SchoolLevel | None:
        for level in SchoolLevel.__members__.values():
            if code == level.code:
                return level


@dataclass
class Institute:
    code: str

    name: str
    english_name: str
    address: str

    request_url_body: str

    @property
    def request_url(self) -> URL:
        return URL(f"https://{self.request_url_body}")


@dataclass
class SearchKey:
    token: str


@dataclass
class SearchResult:
    institutes: List[Institute]
    search_key: SearchKey


async def search_school(
    session: CommonHcsSession,
    region: Region,
    school_level: SchoolLevel,
    query_name: str,
) -> SearchResult:
    json = await session.get_common(
        f"/v2/searchSchool?lctnScCode={region.code}&schulCrseScCode={school_level.code}&orgName={query_name}&loginType=school"
    )

    return SearchResult(
        search_key=json["key"],
        institutes=[
            Institute(
                code=item["orgCode"],
                name=item["kraOrgNm"],
                english_name=item["engOrgNm"],
                address=item["addres"],  # not my typo
                request_url_body=item["atptOfcdcConctUrl"],
            )
            for item in json["schulList"]
        ],
    )
