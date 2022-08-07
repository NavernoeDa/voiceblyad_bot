from datetime import datetime
from os import environ
from random import choice, randint
from time import time

from db import DataBase

from aiogram import Bot, Dispatcher, types, executor
from dotenv import load_dotenv
from pytz import timezone

load_dotenv('config.env')
token = Bot(environ['TOKEN_BOT'])
bot = Dispatcher(token)


def get_time(region='Asia/Kamchatka'):
    tz = timezone(region)
    return datetime.now(tz).hour


async def mute(message, reason, hours, id_user, name):
    await token.restrict_chat_member(
        message.chat.id,
        id_user,
        types.ChatPermissions(False),
        until_date=int(time()) + hours * 3600
    )
    await token.send_message(message.chat.id,
                             f'Пользователь <b>{name}</b>'
                             f' замучен до {get_time("Europe/Moscow") + hours} часа(ов) по причине: {reason}',
                             parse_mode='HTML'
                             )


@bot.message_handler(commands=['start', 'help'])
async def help(message: types.Message):
    await message.reply('Привет!')


@bot.message_handler(commands='ж')
async def latter(message: types.Message):
    await message.reply(choice(['ж', 'опа']))


@bot.message_handler(commands='random')
async def random(message: types.Message):
    args = message.text.split()
    if len(args) == 2:
        random = randint(0, int(args[1]))
        await message.reply(str(random))
    elif len(args) == 3:
        random = randint(int(args[1]), int(args[2]))
        await message.reply(str(random))


@bot.message_handler(commands='count_of_chats')
async def count(message: types.Message):
    await message.reply(f'Количество чатов, в которых есть бот: {randint(1, 20)}')


@bot.message_handler(commands='mute')
async def mute_tg(message: types.Message):
    if message.from_user.id == 727314096:
        args = message.text.split()
        await mute(message, args[1], int(args[2]),
        message.reply_to_message.from_user.id, message.reply_to_message.from_user.first_name)
    else:
        await message.reply('Тебе нельзя.')


@bot.message_handler(commands='unmute')
async def unmute(message: types.Message):
    await token.restrict_chat_member(
        message.chat.id,
        message.reply_to_message.from_id,
        types.ChatPermissions(True, True, True, True, True)
    )
    await token.send_message(message.chat.id,
                             f'Пользователь <b>{message.reply_to_message.from_user.first_name}</b>'
                             f' размучен', parse_mode='HTML')



@bot.message_handler(commands='ban')
async def ban(message: types.Message): # см. строка 48
    await token.ban_chat_member(message.chat.id, message.reply_to_message.from_user.id)


@bot.message_handler(commands='my_voices')
async def my_voices(message: types.Message):
    count = DataBase().get_voices(message.from_user.username)
    if count is None:
        await message.reply('У тебя нет голосовых')
    else:
        await message.reply(f'Текущее количество твоих голосовых: {count[0]}')


@bot.message_handler(commands='all_voices')
async def all_voices(message: types.Message):
    info_voices = DataBase().get_voices()
    text_voices = ''
    for voice in info_voices:
        text_voices += f'<b>{voice[0]}</b> начирикал {voice[1]} голосовых\n'
    await token.send_message(message.chat.id, text_voices, parse_mode='HTML')


@bot.message_handler(content_types='new_chat_members')
async def gif(message: types.Message):
    if message.from_user.is_premium:
        await message.reply_animation(
            animation='CgACAgIAAx0CTnrVmwACBNpi7KZspRJVcZ3f2DAcv8mKN6j1qQAC-hsAAgmfiUn_sX6GL4jzEikE'
        )


@bot.message_handler(content_types=['text', 'voice'])
async def text(message: types.Message):
    if message.text:
        answers = {
            'миуи': 'говно',
            'miui': 'говно'
        }

        if 'мать' in message.text.lower():
            await mute(message, 'ебатель_матерей3000', 5, message.from_user.id, message.from_user.first_name)

        text = ''
        for word in message.text.lower().split():
            if word in answers.keys():
                text += f'{word} - {answers[word]}\n'

        await message.reply(text)

    elif message.voice:
        DataBase().add_voice(message.from_user.username)


if __name__ == "__main__":
    executor.start_polling(bot)
