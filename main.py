import asyncio
#import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, WebAppInfo
import os
# ——— НАСТРОЙКИ ———
BOT_TOKEN = os.getenv("TOKEN")
TON_WALLET = os.getenv("WALLET")
TON_Viev = os.getenv("TON_V")
TON_AMOUNT = os.getenv("TON_A")
#TONAPI_KEY = 
pending_payments: dict[str, str] = {}

# ——— ИНИЦИАЛИЗАЦИЯ БОТА ———
bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# ——— КЛАВИАТУРА ———
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🟢 Take part"), KeyboardButton(text="📖 About the project")],
        [KeyboardButton(text="🌐 WebApp"), KeyboardButton(text="📊 Statistics and help")]
    ],
    resize_keyboard=True
    
)
""", web_app=WebAppInfo(url="https://ton.org")"""
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
    await message.answer("💎 Welcome to the world of the unique BuckeTON project!\n"
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
"""check_payment_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="💸 Проверить оплату", callback_data="check_payment")]
    ]
)"""

@dp.message(F.text == "🟢 Take part")
async def join_handler(message: Message):
    user_id = str(message.from_user.id)
    comment = f"bucketon_user_{user_id}"
    pending_payments[user_id] = comment

    ton_link = (
        f"https://app.tonkeeper.com/transfer/{TON_WALLET}"
        f"?amount={TON_AMOUNT}&text={comment}"
    )
    #Кнопки под сообщением
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💎 Pay via TONKeeper", url=ton_link)],
            #[InlineKeyboardButton(text="💸 Проверить оплату", callback_data="check_payment_kb")]
        ]
    )

    await message.answer(
        f"💎 Scenario 2\n"
        f"💎 Get your free BuckeTON\n"
        f"💸 To participate, transfer <b>{TON_Viev}</b> from any wallet to the wallet address\n\n"
        f"<code>UQA0ltq3MjKpaR-qBVZs54jsuC81xQHYiIFmM4Aho2vedeKm</code>\n\n"
        f"☑️ Please provide a comment: <code>{comment}</code>\n",reply_markup=keyboard, 
        disable_web_page_preview=True
    )
# ——— ЗАПУСК БОТА ———
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


