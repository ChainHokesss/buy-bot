from src.hyperliquid.client import info
from src.token.handlers.callback import trade_callback_handler


def token__is_exists(token_name: str) -> bool:
    try:
        info.name_to_asset(token_name)
    except KeyError:
        return False
    return True


def token__subscribe(token_name: str) -> bool:
    return (
        True
        if info.subscribe(
            subscription={'type': 'trades', 'coin': token_name},
            callback=trade_callback_handler
        ) != 0
        else False
    )
