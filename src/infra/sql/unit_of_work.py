from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.sql.postgres.session import AsyncSessionBuilder
from src.infra.sql.types import SqlAlchemyModel
from src.infra.unit_of_work import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    session: AsyncSession

    def __init__(self) -> None:
        self.session_factory = AsyncSessionBuilder

    async def __aenter__(self) -> 'UnitOfWork':
        self.session = self.session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if exc_type:
            await self.session.rollback()
            await self.session.close()
            raise exc
        await self.session.commit()
        await self.session.close()

    def add(self, entity: SqlAlchemyModel) -> None:
        self.session.add(entity)

    async def flush(self) -> None:
        await self.session.flush()

    async def refresh(self, entity: SqlAlchemyModel) -> None:
        return await self.session.refresh(entity)

    async def delete(self, entity: SqlAlchemyModel) -> None:
        return await self.session.delete(entity)
