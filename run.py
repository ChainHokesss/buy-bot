import asyncio
import logging
import multiprocessing
import os

from aiohttp import web

from src.token.handlers.token import *
from src.bot import bot, dp
from src.token.logic.selectors.token_chat_config import token_chat_configs__distinct_token_name


async def main():
    async with UnitOfWork() as uow:
        query = token_chat_configs__distinct_token_name()
        token_configs = await query.execute(uow.session)
        for token_config in token_configs:
            token__subscribe(token_name=token_config.token_name)
    await dp.start_polling(bot)


def start_web_server():
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    web.run_app(app, host="0.0.0.0", port=port)


def start_web():
    start_web_server()


def start_bot():
    asyncio.run(main())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    web_process = multiprocessing.Process(target=start_web)
    bot_process = multiprocessing.Process(target=start_bot)

    web_process.start()
    bot_process.start()

    web_process.join()
    bot_process.join()
