import aiofiles
from fastapi import APIRouter, Response, HTTPException, UploadFile
from beanie import WriteRules, PydanticObjectId
from pathlib import Path
from .models import *

router = APIRouter(tags=['MountainPass'])

upload_dir = Path.cwd() / 'upload'


@router.get('/')
async def root():
    return {'message': 'OK'}


@router.post('/submitData')
async def submit_data(data: MountainPass, photo_files: list[UploadFile] | None = None):
    """
    Receive MountainPass data and store it in DB
    """

    person_db = await Person.get_by_email(data.person.email)
    if person_db:
        data.person = person_db

    if data.status and data.status != Status.NEW:
        return HTTPException(400, 'Invalid status')

    if len(data.photos) != len(photo_files):
        return HTTPException(400, 'Invalid photo count')

    # Upload photos and rename them as PhotoData object id
    # https://stackoverflow.com/questions/73442335/how-to-upload-a-large-file-%e2%89%a53gb-to-fastapi-backend/73443824#73443824
    for photo in zip(photo_files, data.photos):
        try:
            photo_id: UUID = photo[1].id
            suffix = Path(photo[0].filename).suffix
            uploaded_file: Path = upload_dir / Path(photo_id.hex).with_suffix(suffix)
            async with aiofiles.open(uploaded_file, 'wb') as f:
                while chunk := await photo[0].read(2**20):
                    await f.write(chunk)
        except Exception:
            return Response(status_code=500)
        finally:
            await photo[0].close()

    await data.save(link_rule=WriteRules.WRITE)
    return Response(status_code=201)


@router.get('/submitData/{_id}', response_model=MountainPassOut)
async def get_data_by_id(_id: PydanticObjectId) -> MountainPass:
    data = await MountainPass.get(_id, fetch_links=True)
    return data
