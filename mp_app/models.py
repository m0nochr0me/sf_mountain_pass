"""
MountainPass App
Models
"""

import json
from typing import List, Optional
from enum import Enum
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field
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
    id: UUID = Field(default_factory=uuid4)
    name: str

    class Settings:
        name = 'photo_data'

    def __repr__(self):
        return f'<PhotoData {self.id.hex}>'

    def __str__(self):
        return self.name


class Person(Document):
    email: Indexed(EmailStr, unique=True)
    username: str
    first_name: str
    last_name: str = None

    class Settings:
        name = 'person'

    def __repr__(self):
        return f'<Person {self.username}>'

    def __str__(self):
        return self.username

    @classmethod
    async def get_by_email(cls, email):
        return await cls.find_one(cls.email == email)


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
                            'name': 'Overlook'
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

    # Custom validator, from
    # https://stackoverflow.com/questions/65504438/how-to-add-both-file-and-json-body-in-a-fastapi-post-request/70640522#70640522
    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value


__beanie_models__ = [MountainPass, Person, PhotoData, GeoData]
