import asyncio                       # Імпортуємо бібліотеку для роботи з асинхронністю
import random                        # Для випадкового вибору елементів зі списку

#Імпортуємо компоненти aiogram для роботи з Telegram Bot API
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode                   # Для вказання HTML-форматування повідомлень
from aiogram.types import Message, CallbackQuery      # Класи для повідомлень та обробки callback-кнопок
from aiogram.filters import Command                   # Фільтр для обробки команд типу /start, /help
from aiogram.utils.keyboard import InlineKeyboardBuilder   # Конструктор інлайн-кнопок
from aiogram.client.default import DefaultBotProperties    # Для задання властивостей бота

#Вказуємо токен, отриманий у BotFather
BOT_TOKEN = "7819021093:AAHXJocKF9Rndc6j9IwrVhOMow8XAw7oS9Q"

#Список українських музичних композицій
ukrainian_music = [
    "Go_A – Шум", "Kalush Orchestra – Stefania", "Океан Ельзи – Без бою",
    "ДахаБраха – Baby", "alyona alyona – Пушка", "Антитіла – TDME",
    "The Hardkiss – Журавлі", "Wellboy – Гуси"
]

#Список українських фільмів
ukrainian_movies = [
    "Захар Беркут (2019)", "Кіборги (2017)", "Поводир (2014)",
    "Додому (2019)", "Мої думки тихі (2019)", "Плем'я (2014)",
    "Тіні забутих предків (1965)", "Віддана (2020)"
]

#Ініціалізація об'єкта бота з HTML-форматуванням за замовчуванням
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

#Створення диспетчера для обробки повідомлень
dp = Dispatcher()

#Функція, що повертає клавіатуру з кнопками головного меню
def main_menu():
    kb = InlineKeyboardBuilder()    # Створюємо builder для клавіатури
    kb.button(text="🎵 Музика", callback_data="get_music")     # Кнопка для музики
    kb.button(text="🎬 Фільми", callback_data="get_movies")    # Кнопка для фільмів
    kb.button(text="ℹ️ Про бота", callback_data="get_info")   # Кнопка "Про бота"
    kb.button(text="🚪 Вихід", callback_data="exit")           # Кнопка виходу
    kb.adjust(2)                     # Відображати кнопки по 2 в ряд
    return kb.as_markup()           # Повертаємо готову клавіатуру

#Обробка команди /start
@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer(                      # Відправляємо привітальне повідомлення
        "👋 Вітаю! Я бот-рекомендатор української музики та фільмів.\n\nОберіть дію:",
        reply_markup=main_menu()               # Додаємо до повідомлення інлайн-кнопки
    )

#Обробка команди /help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(                      # Виводимо інструкцію
        "Натисніть кнопки нижче або наберіть /start для запуску меню."
    )

#Обробка натискання кнопки "Музика"
@dp.callback_query(lambda c: c.data == "get_music")
async def recommend_music(callback: CallbackQuery):
    music = random.sample(ukrainian_music, 3)          # Випадково вибираємо 3 пісні зі списку
    await callback.message.answer(                     # Відправляємо список пісень
        "🎵 Музичні рекомендації:\n" +
        "\n".join(f"– {m}" for m in music)              # Форматуємо список у вигляді маркованого тексту
    )
    await callback.answer()                            # Підтверджуємо натискання кнопки

#Обробка натискання кнопки "Фільми"
@dp.callback_query(lambda c: c.data == "get_movies")
async def recommend_movies(callback: CallbackQuery):
    movies = random.sample(ukrainian_movies, 3)         # Випадкові 3 фільми
    await callback.message.answer(                      # Відповідь користувачу
        "🎬 Кінорекомендації:\n" +
        "\n".join(f"– {m}" for m in movies)
    )
    await callback.answer()                             # Підтвердження callback

#Обробка натискання кнопки "Про бота"
@dp.callback_query(lambda c: c.data == "get_info")
async def bot_info(callback: CallbackQuery):
    await callback.message.answer(                      # Виводимо інформацію про бота
        "ℹ️ Цей бот створений для рекомендацій українського культурного контенту.\nАвтор: студент лабораторної №18."
    )
    await callback.answer()

#Обробка натискання кнопки "Вихід"
@dp.callback_query(lambda c: c.data == "exit")
async def exit_callback(callback: CallbackQuery):
    await callback.message.answer(                      # Повідомлення про завершення
        "👋 Дякуємо за використання бота! До зустрічі."
    )
    await callback.answer()

#Запуск основного циклу бота
async def main():
    await dp.start_polling(bot)                         # Запускаємо обробку повідомлень

#Точка входу в програму
if __name__ == "__main__":
    asyncio.run(main())                                 # Запускаємо асинхронну подію main()
