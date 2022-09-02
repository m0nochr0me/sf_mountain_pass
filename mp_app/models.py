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

    class Settings:
        name = 'title_prefix'

    def __repr__(self):
        return f'<TitlePrefix {self.value}>'

    def __str__(self):
        return self.value


class GeoData(Document):
    data: Point
    altitude: Indexed(int)

    class Settings:
        name = 'geo_data'

    def __repr__(self):
        return f'<GeoData {self.data.coordinates}|{self.altitude}>'

    def __str__(self):
        return self.data.coordinates


class PhotoData(Document):
    name: str
    uuid: UUID4

    class Settings:
        name = 'photo_data'

    def __repr__(self):
        return f'<PhotoData {self.uuid}>'

    def __str__(self):
        return self.name


class Person(Document):
    email: EmailStr
    username: str
    first_name: str
    last_name: str = None

    class Settings:
        name = 'person'

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
    photo: List[Link[PhotoData]]
    status: Status = Status.NEW

    class Config:
        schema_extra = {
            'example':
                {
                    'title': 'Dyatlov',
                    'title_prefix': {
                        'value': 'per.'
                    },
                    'alt_titles': [
                        'Schmyatlov'
                    ],
                    'timestamp': '2022-09-02T02:42:04.340Z',
                    'person': {
                        'email': 'john_doe_1969@example.com',
                        'username': 'johndoe1969',
                        'first_name': 'John',
                        'last_name': 'Doe'
                    },
                    'geodata': {
                        'data': {
                            'coordinates': [
                                '1.33',
                                '-2.66'
                            ],
                            'type': 'Point'
                        },
                        'altitude': 2789
                    },
                    'photo': [
                        {
                            'name': 'Overlook',
                            'uuid': '46f1bda0-1c3c-4bba-a113-80c7433b520e'
                        }
                    ]
                }
        }

    class Settings:
        name = 'mountain_pass'

    def __repr__(self):
        return f'<MountainPass {self.title}>'

    def __str__(self):
        return self.title


__beanie_models__ = [MountainPass, Person, PhotoData, GeoData]
