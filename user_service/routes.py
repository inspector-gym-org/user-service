from fastapi import APIRouter, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from pymongo.errors import DuplicateKeyError

from .database import users_collection
from .logging_route import LoggingRoute
from .models import User

router = APIRouter(
    prefix="/users",
    tags=["users"],
    route_class=LoggingRoute,
)


@router.post("/", response_model=User)
async def create_user(user: User, response: Response) -> User:
    user_json = jsonable_encoder(user)

    try:
        await users_collection.insert_one(user_json)
        response.status_code = status.HTTP_201_CREATED

    except DuplicateKeyError:
        await users_collection.update_one(
            {"telegram_id": user.telegram_id},
            {"$set": user.dict(exclude={"telegram_id", "created"})},
        )
        response.status_code = status.HTTP_200_OK

    return await users_collection.find_one({"telegram_id": user.telegram_id})


@router.get("/{telegram_id}/", response_model=User)
async def get_user(telegram_id: int) -> User:
    if user := await users_collection.find_one({"telegram_id": telegram_id}):
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
    )
