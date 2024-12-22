import typing

from sqlalchemy import Enum as SQLEnum

from src.infra.sql.models import Base

SqlAlchemyModel = typing.TypeVar('SqlAlchemyModel', bound=Base)


class Enum(SQLEnum):
    def __init__(self, *enums: object, **kw: typing.Any) -> None:
        kw['values_callable'] = lambda x: [i.value for i in x]
        super().__init__(*enums, **kw)
