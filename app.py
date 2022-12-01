import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from account import Account

API_TOKEN = ''
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    login_password = State()


users = {}

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await Form.login_password.set() ### wait response from user
    await message.answer("Привет, я помогу тебе в мониторинге твоего инстаграм аккаунта. \n"
                         "Прежде всего тебе нужно зарегистрироваться, введи свой логин и пароль через пробел")
    message_text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    print(user_id, user_name, message_text)


@dp.message_handler(state=Form.login_password)
async def process_login_and_password(message: types.Message, state: FSMContext):
    await state.finish() ### get response from user
    chat_id = message.chat.id
    login = ""
    password = ""
    try:
        login, password = message.text.split() ### get login and password from input
        print(login, password)
    except:
        await message.answer("Некорректный ввод. Попробуйте снова")
        return
    try:
        acc = Account(login, password) ### auth in instagram
        ### TODO save to database by user_id(message.from_user.id)
        users[message.from_user.id] = acc
    except:
        await message.answer("Не удалось авторизоваться. Попробуйте снова")
        return



@dp.message_handler(commands=["menu"])
async def open_magazines(msg: types.Message):
    magazines = {
        "Remove Subs": "remove_subs",
        "Follow on Subs": "follow_on_subs",
        "Show Subscribers": "show_subscribers",
        "Show Followers": "show_followers"
    }
    markup = types.InlineKeyboardMarkup()
    for name, data in magazines.items():
        markup.add(types.InlineKeyboardButton(name, callback_data=data))
    await msg.answer("Команды", reply_markup=markup)


@dp.callback_query_handler(lambda call: True)
async def callback_inline(call):
    ### TODO get user acc by his id (call.from_user.id)
    try:
        acc = users[call.from_user.id]
    except:
        await dp.bot.send_message(chat_id=call.message.chat.id, text="Вы не авторизованы(")
        return
    if call.data == 'remove_subs':
        print("LOL")
        res = acc.RemoveSubsNotFollowingYou()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Success!")
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'follow_on_subs':
        print("KEK")
        res = acc.FollowOnSubs()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Success!")
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'show_subscribers':
        print("chebuREK")
        res = acc.ShowSubscriptions()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text=res)
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'show_followers':
        print("Polniy Cheburek")
        res = acc.ShowFollowers()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text=res)
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
