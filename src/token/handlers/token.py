import logging

from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from src.bot import dp
from src.common.exceptions import ValidationError
from src.common.logic.interactors.common import validate_numeric_value
from src.hyperliquid.logic.interactors import token__is_exists, token__subscribe
from src.infra.sql.unit_of_work import UnitOfWork
from src.token.logic.dto import TokenChatConfigCreateDto
from src.token.logic.facades.token_chat_config import token_chat_config__create_or_update
from src.token.logic.interactors.telegram import telegram__parse_file_id_and_file_type


class Form(StatesGroup):
    token = State()
    min_buy_price = State()
    emoji = State()
    emoji_delta = State()
    photo = State()


@dp.message(Command('add'))
async def add_token(message: types.Message, state: FSMContext) -> None:
    logging.info(f'Token config creation started, chat_id: {message.chat.id}')
    await state.set_state(Form.token)
    await message.answer('❔Send me token name.')


@dp.message(Form.token)
async def process_token_name(message: types.Message, state: FSMContext):
    is_exists = token__is_exists(token_name=message.text)
    if is_exists is False:
        await state.clear()
        await message.reply('Token name is invalid.')
        return
    await state.update_data(token=message.text)
    await state.set_state(Form.min_buy_price)
    await message.answer('❔Send me minimal buy price.')


@dp.message(Form.min_buy_price)
async def process_min_buy_price(message: types.Message, state: FSMContext):
    try:
        min_buy_price = validate_numeric_value(message.text)
    except ValidationError:
        await state.clear()
        await message.reply('Invalid value.')
        return
    await state.update_data(min_buy_price=min_buy_price)
    await state.set_state(Form.emoji)
    await message.answer('❔Send me token emoji')


@dp.message(Form.emoji)
async def process_emoji(message: types.Message, state: FSMContext):
    await state.update_data(emoji=message.text or '*')
    await state.set_state(Form.emoji_delta)
    await message.answer('❔Send me token emoji delta.')


@dp.message(Form.emoji_delta)
async def process_emoji_delta(message: types.Message, state: FSMContext):
    try:
        emoji_delta = validate_numeric_value(message.text)
    except ValidationError:
        await state.clear()
        await message.reply('Invalid value.')
        return

    await state.update_data(emoji_delta=emoji_delta)
    await state.set_state(Form.photo)
    await message.answer('❔Send me token gif or picture (Any character to skip)')


@dp.message(Form.photo)
async def process_photo(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    file_id, file_type = telegram__parse_file_id_and_file_type(message=message)
    async with UnitOfWork() as uow:
        token_chat_config = await token_chat_config__create_or_update(
            uow=uow,
            token_chat_config_create_dto=TokenChatConfigCreateDto(
                token_name=state_data['token'],
                chat_id=message.chat.id,
                min_buy_price=state_data['min_buy_price'],
                emoji=state_data['emoji'],
                file_id=file_id,
                file_type=file_type,
            )
        )
    if not token__subscribe(token_name=token_chat_config.token_name):
        await state.set_state(Form.emoji)
        await message.answer('Subscribe failed.')
    logging.info(f'Token config created, chat_id: {message.chat.id}')
