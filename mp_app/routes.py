from fastapi import APIRouter, Response, HTTPException
from .models import *

router = APIRouter(tags=['MountainPass'])


@router.get('/')
async def root():
    return {'message': 'OK'}



