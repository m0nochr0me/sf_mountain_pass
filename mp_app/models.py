"""
MountainPass App
Models
"""

from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from geojson_pydantic import Feature
from beanie import Document, Indexed, Link


class Status(Enum):
    NEW = 0
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3


class TitlePrefix(BaseModel):
    value: str


class GeoData(Document):
    data: Feature
    altitude: Indexed(int)


class PhotoData(Document):
    name: str
    uuid: UUID4


class Person(Document):
    email: EmailStr
    username: str
    first_name: str
    last_name: str = None


class MountainPass(Document):
    title: str
    title_prefix: TitlePrefix
    alt_titles: Optional[List[str]] = None
    timestamp: datetime
    person: Link[Person]
    geodata: Link[GeoData]
    status: Status = Status.NEW


__beanie_models__ = [MountainPass, Person, PhotoData, GeoData]
