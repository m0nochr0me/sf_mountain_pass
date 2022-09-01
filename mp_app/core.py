"""
MountainPass App
Core
"""

import asyncio
import os
from dotenv import load_dotenv
import motor.motor_asyncio
from pathlib import Path
from fastapi import FastAPI
from beanie import init_beanie
from .models import __beanie_models__


# Environment
load_dotenv()

# DB
db_client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('FSTR_MONGO_URI'))
db = db_client['mp_app']


# FastAPI
app = FastAPI()


@app.on_event('startup')
async def start():
    await init_beanie(database=db, document_models=__beanie_models__)
