from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from .database import database
from .models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/")
async def create_user(user: User, response: Response) -> User:
    user_json = jsonable_encoder(user)

    try:
        await database["users"].insert_one(user_json)
        response.status_code = status.HTTP_201_CREATED

    except DuplicateKeyError:
        response.status_code = status.HTTP_200_OK

    return await database["users"].find_one({"telegram_id": user.telegram_id})


@router.get("/{telegram_id}", response_model=User)
async def get_user(telegram_id: int) -> User:
    if user := await database["users"].find_one({"telegram_id": telegram_id}):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
