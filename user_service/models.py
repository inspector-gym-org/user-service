from datetime import datetime

from pydantic import BaseModel, Field


class User(BaseModel):
    telegram_id: int

    first_name: str
    last_name: str | None
    username: str | None

    created: datetime = Field(default_factory=datetime.now)

    class Config:
        allow_population_by_field_name = True
