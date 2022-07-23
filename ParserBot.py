from InstitParser import main_cycle
from auth_data import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

bot = Bot(token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["Стандартные ссылки"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Press button", reply_markup=keyboard)


@dp.message_handler(Text(equals="Стандартные ссылки"))
async def find_place(message: types.Message):
    await message.answer("Please wait...")

    answers = main_cycle(1)
    print(answers)

    for i in answers:
        await message.answer(i)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
