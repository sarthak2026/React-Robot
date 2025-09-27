

import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReactionTypeEmoji

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8444953547:AAG81gi-_8ray8kneZH_pNaS5sNyVv3j_tY"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# जब भी channel पर नया post आए
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

async def main():
    # Dispatcher को bot से चलाओ
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
