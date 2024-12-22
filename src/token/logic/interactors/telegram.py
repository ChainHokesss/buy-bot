import decimal

from aiogram import types

from src.token.models import TokenChatConfig


def telegram__token_message(token_chat_config: TokenChatConfig, notification: dict) -> str:
    price = decimal.Decimal(notification['px'])
    size = decimal.Decimal(notification['sz'])
    emoji_delta = decimal.Decimal(token_chat_config.emoji_delta)
    number_of_emoji = int(price * size / emoji_delta)
    return (
        f'<code>{token_chat_config.token_name}</code> BUY!\n'
        f'{token_chat_config.emoji * number_of_emoji}\n\n'
        f'🔀 Spent ${price * size}\n'
        f'🔀 Got {size} {token_chat_config.token_name}\n'
        f'👤 <a href="https://app.hyperliquid.xyz/explorer/address/{notification["users"][0]}">Buyer</a>'
        f'/<a href="https://app.hyperliquid.xyz/explorer/tx/{notification["hash"]}">TX</a>\n'
        f'🏷 Price ${price}\n'
        f'💸 Market Cap ${price}'
    )


def telegram__parse_file_id_and_file_type(message: types.Message) -> tuple[str | None, str | None]:
    file_id = None
    file_type = None
    if message.photo:
        file_type = 'photo'
        file_id = message.photo[-1].file_id
    elif message.animation:
        file_type = 'animation'
        file_id = message.animation.file_id
    return file_id, file_type
