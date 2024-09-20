import asyncio
import logging
import os
from aiogram import Dispatcher, types, Bot, F
from aiogram.filters import Command
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv(dotenv_path='app.env')

client = AsyncOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
)

dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command('start'))
async def hello(message: types.Message) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Обо мне', callback_data='about')]
    ])
    await message.answer('Дароу', reply_markup=kb)


@dp.callback_query(F.data == 'about')
async def about_me(query: types.CallbackQuery) -> None:
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Задать вопрос', callback_data='question')]
    ])
    await query.message.edit_text('Я мистер кот, готов ответить тебе на любой вопрос\n'
                                        'Нажми "Задать вопрос"', reply_markup=kb)


@dp.callback_query(F.data == 'question')
async def ask(query: types.CallbackQuery) -> None:
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='как ты кошак?', callback_data='question')]
    ])
    await query.message.answer('спрашивай, что угодно, дружище', reply_markup=kb)


@dp.message(F.text == 'как ты кошак?')
async def how_r_u(message: types.Message) -> None:
    await message.answer('лучше всех, дорогой')


@dp.message()
async def answer_new(message: types.Message) -> None:
    chat_completion = await client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": message.text + '. Ответь как будто ты кот',
            }
        ],
        model="gpt-3.5-turbo",
    )
    reply = chat_completion.choices[0].text.strip()
    await message.answer(reply)


async def main() -> None:
    token = os.getenv("TG_BOT_TOKEN")
    bot = Bot(token=token)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())