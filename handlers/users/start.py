import logging
from aiogram import types

from main import create_user
from data.config import CHANNELS
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from loader import bot, dp
from data.config import CHANNELS
from utils.misc import subscription
@dp.message_handler(commands=['start'])
async def show_channels(message: types.Message):
    user = message.from_user.id
    name = message.from_user.full_name
    create_user(name=name,telegram_id=user)
    final_status = True
    btn = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        status = await subscription.check(user_id=user,
                                          channel=channel)
        final_status *= status
        channel = await bot.get_chat(channel)
        if status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
    btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
    if final_status:
        text = f"👋 <b>Assalomu alaykum, <i>{message.from_user.full_name}</i>!</b>\n\n"\
               f"<b>🤖 Bu bot orqali Rasmlarni PDF shakliga o'zgartirishiz mumkin...</b>\n\n"\
               f"<b>Amalda juda oddiy...Shunchaki rasm tashlang xolos...</b>"
        await message.answer(text)
    if not final_status:
        await message.answer( "👋 Assalomu alaykum\n" +"Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling!", disable_web_page_preview=True, reply_markup=btn)
@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    btn = InlineKeyboardMarkup()
    final_status = True
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        final_status *=status
        channel = await bot.get_chat(channel)
        if not status:
            invite_link = await channel.export_invite_link()
            btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))

    btn.add(InlineKeyboardButton(text="Obunani tekshirish", callback_data="check_subs"))
    if final_status:
        text = f"👋 <b>Assalomu alaykum, <i>{call.message.from_user.full_name}</i>!</b>\n\n"\
               f"<b>🤖 Bu bot orqali Rasmlarni PDF shakliga o'zgartirishiz mumkin...</b>\n\n"\
               f"<b>Amalda juda oddiy...Shunchaki rasm tashlang xolos...</b>"
        await call.message.answer(text)
    if not final_status:
        await call.answer(cache_time=60)
        await call.message.answer("Siz quyidagi kanal(lar)ga obuna bo'lmagansiz!",reply_markup=btn)
        await call.message.delete()
