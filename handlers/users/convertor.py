import io

from aiogram import types
from loader import dp,bot
from keyboards.inline.button import callback,button
from aiogram.dispatcher import FSMContext
from PIL import Image
import requests
@dp.message_handler(content_types=types.ContentType.PHOTO)
async def get_photo(message:types.Message,state:FSMContext):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id=file_id)
    file_url = bot.get_file_url(file_path=file.file_path)
    data = await state.get_data()
    urls = data.get('urls',[])
    urls.append(file_url)
    await state.update_data({
        'urls':urls
    })
    await message.reply(text=f"✅ <b>Rasm qabul qilindi!</b>\n\n"
                             f"➕ <b>Agar davom etmoqchi bo'lsangiz yana rasm yuklang...</b>\n\n"
                             f"<b>Yoki....\n</b>"
                             f"👇<b>Kerakli buyruqni tanlang...</b>",reply_markup=button)
@dp.callback_query_handler(callback.filter())
async def callquery(call:types.CallbackQuery,callback_data:dict,state:FSMContext):
    action = callback_data['action']
    if action=='cancel':
        await call.answer('Amal bekor qilindi!')
        await state.update_data({
            'urls':[]
        })
    elif action=='finish':
        await call.answer("Tayyorlanmoqda...")
        data = await state.get_data()
        urls = data.get('urls',[])
        image = Image.open(requests.get(url=urls[0],stream=True).raw)
        images = [Image.open(requests.get(url=url,stream=True).raw) for url in urls[1:]]
        pdf = io.BytesIO()
        image.save(pdf,format='PDF',save_all=True,append_images=images,resolution=100)
        pdf.seek(0)
        file = types.InputFile(pdf,filename=f'{call.from_user.full_name}.pdf')
        white = '◻️'
        black = '◼️'
        xabar = await bot.send_message(chat_id=call.from_user.id,text="<b>Yuklanmoqda...</b>")
        for i in range(1,11):
            oq = (10-i) * white
            qora = i*black
            await xabar.edit_text(text=f"{qora}{oq}\n"
                                       f"{10*i}% yuklandi...")
        await xabar.delete()
        await call.message.answer_document(document=file,caption='@Imagetopdfuzbot')
        await state.update_data({
            'urls': []
        })
    await call.message.delete()
