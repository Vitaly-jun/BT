import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web  # <-- добавили aiohttp для http-сервера
import os

# ——— НАСТРОЙКИ ———
BOT_TOKEN = os.getenv("TOKEN")
TON_WALLET = os.getenv("WALLET")
TON_Viev = os.getenv("TON_V")
TON_AMOUNT = os.getenv("TON_A")

pending_payments: dict[str, str] = {}

# ——— ИНИЦИАЛИЗАЦИЯ БОТА ———
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ——— КЛАВИАТУРА ———
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟢 Take part"), KeyboardButton(text="📖 About the project")],
        [KeyboardButton(text="🌐 WebApp"), KeyboardButton(text="📊 Statistics and help")]
    ],
    resize_keyboard=True
)

# ——— ОБРАБОТКА /start ———
@dp.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        f"👋 Hi, <b>{message.from_user.first_name}</b>!\n"
        f"Welcome to BuckeTON!",
        reply_markup=main_keyboard
    )

# ——— О ПРОЕКТЕ ———
@dp.message(F.text == "📖 About the project")
async def about_handler(message: Message):
    await message.answer(
        "💎 Welcome to the world of the unique BuckeTON project!\n"
        "📢 Join our official channel for updates and results:\n"
        "<a href='https://t.me/bucketon11'>@BuckeTON_Channel</a>",
        disable_web_page_preview=True
    )

# ——— СТАТИСТИКА ———
@dp.message(F.text == "📊 Statistics and help")
async def stats_handler(message: Message):
    await message.answer("📊 Statistics will be added later.")

# ——— WEBAPP ———
@dp.message(F.text == "🌐 WebApp")
async def webapp_handler(message: Message):
    await message.answer("🌐 This section is still in development.") 

# ——— ПРИНЯТЬ УЧАСТИЕ ———
@dp.message(F.text == "🟢 Take part")
async def join_handler(message: Message):
    user_id = str(message.from_user.id)
    comment = f"bucketon_user_{user_id}"
    pending_payments[user_id] = comment

    ton_link = (
        f"https://app.tonkeeper.com/transfer/{TON_WALLET}"
        f"?amount={TON_AMOUNT}&text={comment}"
    )
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 Pay via TONKeeper", url=ton_link)],
        ]
    )

    await message.answer(
        f"💎 Scenario 2\n"
        f"💎 Get your free BuckeTON\n"
        f"💸 To participate, transfer <b>{TON_Viev}</b> TON to the wallet address:\n\n"
        f"<code>UQA0ltq3MjKpaR-qBVZs54jsuC81xQHYiIFmM4Aho2vedeKm</code>\n\n"
        f"☑️ Please provide a comment: <code>{comment}</code>\n",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

# ——— HTTP-сервер для UptimeRobot ———
async def health_check(request):
    return web.Response(text="OK")  # ответ на пинг

async def start_web_server():
    app = web.Application()
    app.router.add_get("/health", health_check)
    app.router.add_get("/", health_check)  # можно и на корень
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)  # Render пингует этот порт
    await site.start()
    print("✅ Health server running on port 8080")

# ——— ЗАПУСК ———
async def main():
    # Запускаем web-сервер для UptimeRobot
    asyncio.create_task(start_web_server())

    # Запускаем polling
    await dp.start_polling(bot)

if name == "main":
    asyncio.run(main())





