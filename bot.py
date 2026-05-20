import os
import logging
import asyncio

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMIN_ID = 89247204

STORAGE_CHANNEL_ID = -1003959246499

logging.basicConfig(level=logging.INFO)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args

    if args:

        try:
            msg_id = int(args[0])

            await context.bot.copy_message(
                chat_id=update.effective_chat.id,
                from_chat_id=STORAGE_CHANNEL_ID,
                message_id=msg_id,
            )

        except Exception as e:
            print(e)

            await update.message.reply_text(
                "File not found."
            )

        return

    await update.message.reply_text(
        "Send media to store."
    )


async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "Not allowed."
        )
        return

    try:

        stored_message = await context.bot.copy_message(
            chat_id=STORAGE_CHANNEL_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )

        msg_id = stored_message.message_id

        bot_username = (
            await context.bot.get_me()
        ).username

        share_link = (
            f"https://t.me/{bot_username}?start={msg_id}"
        )

        await update.message.reply_text(
            f"Stored Successfully ✅\n\n{share_link}"
        )

    except Exception as e:
        print(e)

        await update.message.reply_text(
            "Failed."
        )


async def main():

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            save_media,
        )
    )

    print("Bot running...")

    await app.run_polling()


if __name__ == "__main__":
    asyncio.run(main())
