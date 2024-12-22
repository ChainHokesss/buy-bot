from src.infra.sql.sqlalchemy import Select, select
from src.token.models import TokenChatConfig


def token_chat_configs__all() -> Select[TokenChatConfig]:
    return select(TokenChatConfig)


def token_chat_configs__by_chat_id(
    *, query: Select[TokenChatConfig] | None = None, chat_id: int
) -> Select[TokenChatConfig]:
    if query is None:
        query = token_chat_configs__all()
    return query.where(TokenChatConfig.chat_id == chat_id)


def token_chat_configs__by_token_name(
    *, query: Select[TokenChatConfig] | None = None, token_name: str
) -> Select[TokenChatConfig]:
    if query is None:
        query = token_chat_configs__all()
    return query.where(TokenChatConfig.token_name == token_name)


def token_chat_configs__by_chat_id_and_token_name(
    *, query: Select[TokenChatConfig] | None = None, chat_id: int, token_name: str
) -> Select[TokenChatConfig]:
    query = token_chat_configs__by_chat_id(query=query, chat_id=chat_id)
    return token_chat_configs__by_token_name(query=query, token_name=token_name)


def token_chat_configs__distinct_token_name(
    *, query: Select[TokenChatConfig] | None = None
) -> Select[TokenChatConfig]:
    if query is None:
        query = token_chat_configs__all()
    return query.distinct(TokenChatConfig.token_name)
