from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from .database import users_collection
from .logging_route import LoggingRoute
from .models import User, UserCreate

router = APIRouter(prefix="/users", tags=["users"], route_class=LoggingRoute)


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user_create: UserCreate) -> User:
    user = User(**user_create.dict())

    await users_collection.update_one(
        {"telegram_id": user.telegram_id}, {"$set": jsonable_encoder(user)}, upsert=True
    )

    return await users_collection.find_one({"telegram_id": user.telegram_id})


@router.get("/{telegram_id}/", response_model=User)
async def get_user(telegram_id: int) -> User:
    if user := await users_collection.find_one({"telegram_id": telegram_id}):
        return user

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
