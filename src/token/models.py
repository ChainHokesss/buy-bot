from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from src.infra.sql.constraints import unique_constraint
from src.infra.sql.models import Base, TimestampMixin


class TokenChatConfig(TimestampMixin, Base):
    __tablename__ = 'token_chat_config'
    __table_args__ = (unique_constraint('token_name', 'chat_id'),)

    token_name: Mapped[str]
    chat_id: Mapped[int] = mapped_column(BigInteger)
    min_buy_price: Mapped[float]
    emoji: Mapped[str]
    emoji_delta: Mapped[float] = mapped_column(server_default="50.0")
    file_id: Mapped[str | None]
    file_type: Mapped[str | None]
