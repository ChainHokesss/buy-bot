import asyncio
import logging

from src.bot import bot
from src.infra.sql.unit_of_work import UnitOfWork
from src.token.logic.interactors.telegram import telegram__token_message
from src.token.logic.selectors.token_chat_config import token_chat_configs__by_token_name
from src.token.models import TokenChatConfig

existing_loop = asyncio.get_event_loop()

def trade_callback_handler(message):
    data = message['data']
    if not data:
        return
    asyncio.run_coroutine_threadsafe(
        async_trade_callback_handler(coin_notifications=data), loop=existing_loop
    )


async def async_trade_callback_handler(coin_notifications: list[dict]):
    token_name = coin_notifications[0]['coin']
    async with UnitOfWork() as uow:
        query = token_chat_configs__by_token_name(token_name=token_name)
        token_chat_configs = await query.execute(uow.session)
        tasks = [
            handle_coin_notification(
                coin_notification=coin_notification, token_chat_config=token_chat_config
            )
            for token_chat_config in token_chat_configs
            for coin_notification in coin_notifications
        ]
        await asyncio.gather(*tasks)


async def handle_coin_notification(coin_notification: dict, token_chat_config: TokenChatConfig):
    if token_chat_config.min_buy_price > float(coin_notification['px']) * float(coin_notification['sz']):
        return
    if coin_notification['side'] != 'B':
        return
    message = telegram__token_message(
        token_chat_config=token_chat_config, notification=coin_notification
    )
    if token_chat_config.file_type == 'animation':
        return await bot.send_animation(
            chat_id=token_chat_config.chat_id,
            animation=token_chat_config.file_id,
            parse_mode="HTML",
            caption=message,
        )
    elif token_chat_config.file_type == 'photo':
        return await bot.send_photo(
            chat_id=token_chat_config.chat_id,
            photo=token_chat_config.file_id,
            parse_mode="HTML",
            caption=message,
        )
    return await bot.send_message(
        chat_id=token_chat_config.chat_id,
        parse_mode="HTML",
        text=message
    )
