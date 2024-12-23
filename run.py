import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

from src.token.handlers.token import *
from src.bot import bot, dp
from src.token.logic.selectors.token_chat_config import token_chat_configs__distinct_token_name


async def main():
    async with UnitOfWork() as uow:
        query = token_chat_configs__distinct_token_name()
        token_configs = await query.execute(uow.session)
        for token_config in token_configs:
            token__subscribe(token_name=token_config.token_name)
    logging.info('Start bot')
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
