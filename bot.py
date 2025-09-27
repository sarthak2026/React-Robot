

import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReactionTypeEmoji

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8444953547:AAG81gi-_8ray8kneZH_pNaS5sNyVv3j_tY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Required channels user must join
CHANNELS = ["@YourChannel1", "@YourChannel2"]

# ---------------- Start Command ----------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = "Welcome! Please join our channels first to use this bot:"
    buttons = [
        [InlineKeyboardButton("Join Channel 1", url="https://t.me/+rKZUFwEjREgxZWU1")],
        [InlineKeyboardButton("Join Channel 2", url="https://t.me/+PjrYauAdRSQyMWI9")],
        [InlineKeyboardButton("✅ Verify", callback_data="verify_channels")]
    ]
    await message.reply(text, reply_markup=InlineKeyboardMarkup(buttons))

# ---------------- Verify Channels ----------------
@dp.callback_query_handler(lambda c: c.data == "verify_channels")
async def verify_channels(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    all_joined = True

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status == "left":
                all_joined = False
        except:
            all_joined = False

    if all_joined:
        await callback_query.message.edit_text(
            "✅ Verified! Now the bot features will work."
        )
        await callback_query.answer("You have joined all channels ✅")
    else:
        await callback_query.answer(
            "❌ Please join all channels first!", show_alert=True
        )

# ---------------- React on Channel Posts ----------------
@dp.channel_post()
async def react_on_post(message: types.Message):
    try:
        await bot.set_message_reaction(
            chat_id=message.chat.id,
            message_id=message.message_id,
            reaction=[ReactionTypeEmoji(emoji="👍")]
        )
        print(f"Reacted to post {message.message_id} in {message.chat.title}")
    except Exception as e:
        print("Error:", e)

# ---------------- Run Bot ----------------
async def main():
    print("Bot is running...")
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
