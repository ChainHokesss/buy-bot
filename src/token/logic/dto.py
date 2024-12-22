from src.common.logic.dto import BaseDto


class TokenChatConfigCreateDto(BaseDto):
    token_name: str
    chat_id: int
    min_buy_price: float
    emoji: str
    file_id: str | None = None
    file_type: str | None = None


class TokenChatConfigUpdateDto(BaseDto):
    token_name: str | None = None
    chat_id: int | None = None
    min_buy_price: float | None = None
    emoji: str | None = None
    file_id: str | None = None
    file_type: str | None = None
