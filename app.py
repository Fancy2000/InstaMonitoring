import logging

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = ''
logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Привет, я помогу тебе в мониторинге твоего инстаграм аккаунта. \n"
                         "Прежде всего тебе нужно зарегистрироваться, введи свой логин и пароль через пробел")


@dp.message_handler(commands=["menu"])
async def open_magazines(msg: types.Message):
    magazines = {
        "Команда1": "command1",
        "Команда2": "command2",
    }
    markup = types.InlineKeyboardMarkup()
    for name, data in magazines.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=data))
    await msg.answer("Команды", reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    if call.data == 'command1':
        print("LOL")
        await dp.bot.send_message(chat_id=call.message.chat.id, text="command1")
    elif call.data == 'command2':
        print("KEK")
        await dp.bot.send_message(chat_id=call.message.chat.id, text="command2")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
