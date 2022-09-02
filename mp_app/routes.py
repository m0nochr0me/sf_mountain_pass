from fastapi import APIRouter, Response, HTTPException, UploadFile
from beanie import WriteRules
from .models import *

router = APIRouter(tags=['MountainPass'])


@router.get('/')
async def root():
    return {'message': 'OK'}


@router.post('/submitData')
async def submit_data(data: MountainPass, photos: list[UploadFile] | None = None):
    """
    Receive MountainPass data and store it in DB
    """

    person_db = await Person.get_by_email(data.person.email)
    if person_db:
        data.person = person_db

    if data.status and data.status != Status.NEW:
        return HTTPException(400, 'Invalid status')

    # TODO: Process photos

    await data.save(link_rule=WriteRules.WRITE)
    return Response(status_code=201)
