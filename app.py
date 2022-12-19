import asyncio
import logging
import requests
import schedule
import time
import matplotlib.pyplot as plt
import os
import string
import random

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
# from aiogram.types import FSInputFile
from aiogram.types import InputFile
#
from account import Account
from database import Database

API_TOKEN = '5759310189:AAFKK2t5a5wMzSIO_saqWj-61J143DmFTnw'
logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    login_password = State()
    get_period = State()


users = {}




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await Form.login_password.set() ### wait response from user
    await message.answer("Привет, я помогу тебе в мониторинге твоего инстаграм аккаунта. \n"
                         "Прежде всего тебе нужно зарегистрироваться, введи свой логин, пароль и код аутентификации"
                         " через пробел")
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
        login, password, authCode= message.text.split() ### get login and password from input
    except:
        await message.answer("Некорректный ввод. Попробуйте снова")
        return
    try:
        acc = Account(login, password, authCode) ### auth in instagram
        await message.answer("Успешная аутентификация")
        acc.GetUserId()
        users[message.from_user.id] = acc
    except:
        await message.answer("Не удалось авторизоваться. Попробуйте снова")
        return

@dp.message_handler(state=Form.get_period)
async def process_get_period(message: types.Message, state: FSMContext):
    await state.finish() ### get response from user
    chat_id = message.chat.id
    period = message.text
    try:
        period = int(period)
    except:
        await message.answer("Ошибка! Введите число!")
        return



@dp.message_handler(commands=["menu"])
async def open_magazines(msg: types.Message):
    magazines = {
        "Remove Subs": "remove_subs",
        "Follow on Subs": "follow_on_subs",
        "Show Subscribers": "show_subscribers",
        "Show Followers": "show_followers",
        "Show Stories Info": "show_stories_info",
        # 'Get Period Subscribtions': "get_period_subscribtions", ### TODO add timestamp to db
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
        res = acc.RemoveSubsNotFollowingYou()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="\n".join(list(res)))
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'follow_on_subs':
        res = acc.FollowOnSubs()
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="\n".join(list(res)))
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'show_subscribers':
        res = acc.ShowSubscriptions()
        ans = []
        for i, elem in enumerate(res.values()):
            ans.append(str(len(res) - i) + ") " + elem.username)
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="\n".join(ans))
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == 'show_followers':
        res = acc.ShowFollowers()
        print(type(res))
        print(res)
        ans = []
        for i, elem in enumerate(res.values()):
            ans.append(str(len(res) - i) + ") " + elem.username)
        if res:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="\n".join(ans))
        else:
            await dp.bot.send_message(chat_id=call.message.chat.id, text="Failed!")
    elif call.data == "show_stories_info":
        res = acc.ShowStoriesInfo()
        ans = []

        for elem in res:
            url_http = elem[0] # URL on post
            users_ = elem[1] # set of username
            img_data = requests.get(url_http).content
            filename = "".join(random.choice(string.hexdigits) for i in range(16))
            if not os.path.exists("stories"):
                os.mkdir("stories") ### creating directory to storage plots
            with open("stories/{}.png".format(filename), 'wb') as handler:
                handler.write(img_data)
            photo = open("stories/{}.png".format(filename), "rb")
            await dp.bot.send_photo(chat_id=call.message.chat.id, photo=photo)
            await dp.bot.send_message(chat_id=call.message.chat.id, text="\n".join(list(users_)))

    # elif call.data == "get_period_subscribtions":
    #     subs, timestamp = db.get_dynamic_subscribers(acc.GetUserId())
    #     len_subs = []
    #     for i in range(len(subs)):
    #         len_subs.append(len(subs[i]))
    #     if not os.path.exists("plots"):
    #         os.mkdir("plots") ### creating directory to storage plots
    #     plt.clf()
    #     plt.plot(timestamp, len_subs)
    #     filename = "".join(random.choice(string.hexdigits) for i in range(16)) ### generating random filename with length 16
    #     plt.savefig("plots/{}.png".format(filename)) ### saving plot to "images" dir
    #     plot = FSInputFile("plots/{}.png".format(filename)) ### getting file to send it to chat
    #     dp.bot.send_photo(chat_id=call.message.chat.id, photo=plot) ### sending file


if __name__ == '__main__':
    db = Database("insta", "postgres", "localhost", "password")
    executor.start_polling(dp, skip_updates=True)


