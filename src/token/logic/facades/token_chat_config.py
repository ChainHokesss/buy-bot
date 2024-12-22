from src.common.exceptions import NotFoundError
from src.common.logic.facades.common import create_model_instance, update_model_instance
from src.infra.unit_of_work import AbstractUnitOfWork
from src.token.logic.dto import TokenChatConfigCreateDto, TokenChatConfigUpdateDto
from src.token.logic.selectors.token_chat_config import token_chat_configs__by_chat_id_and_token_name
from src.token.models import TokenChatConfig


async def token_chat_config__by_chat_id_and_token_name(
    *, uow: AbstractUnitOfWork, chat_id: int, token_name: str
) -> TokenChatConfig:
    query = token_chat_configs__by_chat_id_and_token_name(
        chat_id=chat_id, token_name=token_name
    )
    token_chat_config = await query.first_or_none(db=uow.session)
    if token_chat_config is None:
        raise NotFoundError
    return token_chat_config


async def token_chat_config__create(
    *, uow: AbstractUnitOfWork, token_chat_config_create_dto: TokenChatConfigCreateDto
) -> TokenChatConfig:
    return await create_model_instance(
        uow=uow,
        model_class=TokenChatConfig,
        validated_data=token_chat_config_create_dto.model_dump(exclude_unset=True),
    )


async def token_chat_config__update(
    *,
    uow: AbstractUnitOfWork,
    token_chat_config: TokenChatConfig,
    token_chat_config_update_dto: TokenChatConfigUpdateDto,
) -> TokenChatConfig:
    return await update_model_instance(
        uow=uow, instance=token_chat_config, validated_data=token_chat_config_update_dto.model_dump(exclude_unset=True)
    )


async def token_chat_config__create_or_update(
    *, uow: AbstractUnitOfWork, token_chat_config_create_dto: TokenChatConfigCreateDto
) -> TokenChatConfig:
    try:
        token_chat_config = await token_chat_config__by_chat_id_and_token_name(
            uow=uow, chat_id=token_chat_config_create_dto.chat_id, token_name=token_chat_config_create_dto.token_name
        )
        token_chat_config = await token_chat_config__update(
            uow=uow,
            token_chat_config=token_chat_config,
            token_chat_config_update_dto=TokenChatConfigUpdateDto.model_validate(token_chat_config_create_dto)
        )
    except NotFoundError:
        token_chat_config = await token_chat_config__create(
            uow=uow, token_chat_config_create_dto=token_chat_config_create_dto
        )
    return token_chat_config
