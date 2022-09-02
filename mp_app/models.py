"""
MountainPass App
Models
"""

from typing import List, Optional
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, EmailStr, UUID4
from geojson_pydantic import Point
from beanie import Document, Indexed, Link


class Status(Enum):
    NEW = 0
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3


class TitlePrefix(BaseModel):
    value: str

    class DocumentMeta:
        collection_name = 'title_prefix'

    def __repr__(self):
        return f'<TitlePrefix {self.value}>'

    def __str__(self):
        return self.value


class GeoData(Document):
    data: Point
    altitude: Indexed(int)

    class DocumentMeta:
        collection_name = 'geo_data'

    def __repr__(self):
        return f'<GeoData {self.data.coordinates}|{self.altitude}>'

    def __str__(self):
        return self.data.coordinates


class PhotoData(Document):
    name: str
    uuid: UUID4

    class DocumentMeta:
        collection_name = 'photo_data'

    def __repr__(self):
        return f'<PhotoData {self.uuid}>'

    def __str__(self):
        return self.name


class Person(Document):
    email: EmailStr
    username: str
    first_name: str
    last_name: str = None

    class DocumentMeta:
        collection_name = 'person'

    def __repr__(self):
        return f'<Person {self.username}>'

    def __str__(self):
        return self.username


class MountainPass(Document):
    title: str
    title_prefix: TitlePrefix
    alt_titles: Optional[List[str]] = None
    timestamp: datetime
    person: Link[Person]
    geodata: Link[GeoData]
    status: Status = Status.NEW

    class DocumentMeta:
        collection_name = 'mountain_pass'

    def __repr__(self):
        return f'<MountainPass {self.title}>'

    def __str__(self):
        return self.title


__beanie_models__ = [MountainPass, Person, PhotoData, GeoData]
