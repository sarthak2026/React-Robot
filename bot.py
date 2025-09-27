import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import ReactionTypeEmoji, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN") or "8364247517:AAEqBCVF6NumW2mvJdx6tYPSm4inM15KPCM"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# --- Channels IDs/Usernames for forced join ---
CHANNEL_1 = "@FREETELEGRAM_MEMBERBOT"      # Update Channel
CHANNEL_2 = "@FREE_MEMBER_ADD_BOT"          # Forced Subscription Channel

# Dictionary to save user reaction preferences {user_id: emoji}
user_reactions = {}

# Set to track channels where congratulatory message has already been sent
congrats_sent_channels = set()

# --- START Command Handler ---
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 Join Free Members Channel", url=f"https://t.me/{CHANNEL_1[1:]}")],
        [InlineKeyboardButton(text="🚀 Join Free Service Channel", url=f"https://t.me/{CHANNEL_2[1:]}")],
        [InlineKeyboardButton(text="✅ Check Joined", callback_data="check_joined")]
    ])

    await message.answer(
        "🤖 *Free AUTO REACTION Bot* में आपका स्वागत है!\n\n"
        "✨ _शुरू करने के लिए, नीचे दिए गए दोनों चैनलों को join करें:_\n"
        "1️⃣ Free Members Channel\n"
        "2️⃣ Join Free Service Channel\n\n"
        "_जब join कर लें, तब_ ✅ *Check Joined* दबाएँ\n\n"
        "--------------------------------------\n"
        "🤖 *Welcome to Free AUTO REACTION Bot!*\n"
        "✨ _To get started, please join both of our channels below:_\n"
        "1️⃣ Free Members Channel\n"
        "2️⃣ Join Free Service Channel\n\n"
        "_Once joined, click_ ✅ *Check Joined*",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


# --- Check Joined Handler ---
@dp.callback_query(F.data == "check_joined")
async def check_joined(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        member1 = await bot.get_chat_member(CHANNEL_1, user_id)
        member2 = await bot.get_chat_member(CHANNEL_2, user_id)

        if member1.status in ["member", "administrator", "creator"] and member2.status in ["member", "administrator", "creator"]:
            reaction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [
                    InlineKeyboardButton(text="👍", callback_data="react_👍"),
                    InlineKeyboardButton(text="😍", callback_data="react_😍"),
                    InlineKeyboardButton(text="❤️", callback_data="react_❤️")
                ],
                [
                    InlineKeyboardButton(text="🔥", callback_data="react_🔥"),
                    InlineKeyboardButton(text="😂", callback_data="react_😂"),
                    InlineKeyboardButton(text="👏", callback_data="react_👏")
                ]
            ])
            await callback.message.answer(
                "✅ *आपने दोनों चैनल सफलतापूर्वक join कर लिए हैं!* 🎉\n\n"
                "अब नीचे से अपना पसंदीदा reaction चुनें 👇\n"
                "_ध्यान दें: अपने channel settings में reactions enable करें_\n\n"
                "--------------------------------------\n"
                "✅ *You have successfully joined both channels!* 🎉\n"
                "Now choose the reaction you want for your channel posts 👇\n"
                "_Note: Make sure reactions are enabled in your channel settings_",
                reply_markup=reaction_keyboard,
                parse_mode="Markdown"
            )
        else:
            await callback.message.answer(
                "❌ *दोनों चैनल join करना ज़रूरी है!* 🚀\n"
                "कृपया join करें और फिर से *Check Joined* दबाएँ।\n\n"
                "--------------------------------------\n"
                "❌ *You must join both channels to continue!* 🚀\n"
                "Please join and then click *Check Joined* again.",
                parse_mode="Markdown"
            )
    except Exception as e:
        print("Error checking subscription:", e)


# --- Handle Reaction Choice and Add Admin Button ---
@dp.callback_query(F.data.startswith("react_"))
async def set_reaction(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    chosen_emoji = callback.data.split("_")[1]

    # Save reaction preference
    user_reactions[user_id] = chosen_emoji

    bot_info = await bot.get_me()
    add_bot_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="➕ Add Bot as Admin to Your Channel",
                url=f"https://t.me/{bot_info.username}?startchannel=true"
            )
        ]
    ])

    await callback.message.answer(
        f"✅ *आपका reaction {chosen_emoji} सेट हो गया है!* 🎉\n\n"
        "👉 अब इस bot को अपने channel में *Admin* बनाइए और 'Post Reaction Permission' दीजिए।\n"
        "Bot automatically आपके नए posts पर react करेगा!\n\n"
        "--------------------------------------\n"
        f"✅ *Your reaction has been set to {chosen_emoji}!* 🎉\n"
        "👉 Now, please add this bot to your channel as *Admin* with 'Post Reaction Permission'.\n"
        "Bot will automatically react on new posts!",
        parse_mode="Markdown",
        reply_markup=add_bot_keyboard
    )


# --- Auto Reaction on Channel Post ---
@dp.channel_post()
async def react_on_post(message: types.Message):
    try:
        admins = await bot.get_chat_administrators(message.chat.id)
        owner_id = None
        for admin in admins:
            if admin.status == "creator":
                owner_id = admin.user.id
                break

        if owner_id and owner_id in user_reactions:
            reaction_emoji = user_reactions[owner_id]
            await bot.set_message_reaction(
                chat_id=message.chat.id,
                message_id=message.message_id,
                reaction=[ReactionTypeEmoji(emoji=reaction_emoji)]
            )
            print(f"Reacted with {reaction_emoji} to post {message.message_id} in {message.chat.title}")

            # Send congratulatory message only once per channel
            if message.chat.id not in congrats_sent_channels:
                try:
                    await bot.send_message(
                        chat_id=owner_id,
                        text=(
                            "🎉 *Congratulations!* Bot has been successfully added to your channel and is working.\n"
                            "✅ Now every new post in your channel will automatically get your chosen reaction.\n\n"
                            "🎊 *बधाई हो!* Bot आपके चैनल में सफलतापूर्वक add हो गया है और काम कर रहा है।\n"
                            "✅ अब आपके चैनल के हर नए post पर आपके चुने हुए reaction automatically लगेगा।"
                        ),
                        parse_mode="Markdown"
                    )
                    # Mark this channel as message sent
                    congrats_sent_channels.add(message.chat.id)
                except Exception as e:
                    print("Error sending congratulatory message:", e)

        else:
            if owner_id:
                try:
                    await bot.send_message(
                        chat_id=owner_id,
                        text=(
                            "⚠️ आपने अभी तक कोई reaction set नहीं किया है!\n"
                            "👉 कृपया bot को `/start` करके reaction चुनें।\n\n"
                            "⚠️ You have not set any reaction yet!\n"
                            "👉 Please run `/start` and choose a reaction so the bot can work in your channel."
                        ),
                        parse_mode="Markdown"
                    )
                except Exception as e:
                    print("Unable to send reminder:", e)
            else:
                print(f"No owner found for channel {message.chat.title}")
    except Exception as e:
        print("Error reacting on post:", e)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

