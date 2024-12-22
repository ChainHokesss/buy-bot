from pydantic import BaseModel, ConfigDict

from src.infra.sql.types import SqlAlchemyModel


class BaseDto(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True, from_attributes=True)
