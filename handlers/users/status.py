from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp,Command

from main import get_users
from loader import dp
@dp.message_handler(Command('info'))
async def info(message:types.Message):
    text = f"👋 <b>Assalomu alaykum, <i>{message.from_user.full_name}</i>!</b>\n\n"\
               f"<b>🤖 Bu bot orqali Rasmlarni PDF shakliga o'zgartirishiz mumkin...</b>\n\n"\
               f"<b>Amalda juda oddiy...Shunchaki rasm tashlang xolos...</b>"
    await message.reply(text)
@dp.message_handler(Command('status'))
async def get(message:types.Message):
    text = get_users()
    await message.answer(text)