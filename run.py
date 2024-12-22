import asyncio
import logging
import os

from aiogram.types import Update
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


async def handle_update(request):
    json_data = await request.json()
    update = Update(**json_data)
    await dp.process_update(update)
    return web.Response()


def start_web_server():
    port = int(os.getenv("PORT", 8080))
    app = web.Application()
    app.router.add_post('/webhook', handle_update)
    web.run_app(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    start_web_server()
    asyncio.run(main())
