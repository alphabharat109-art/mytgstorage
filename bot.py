import os
import logging

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# BOT TOKEN FROM RENDER ENV VARIABLE
BOT_TOKEN = os.getenv("BOT_TOKEN")

# YOUR TELEGRAM USER ID
ADMIN_ID = 89247204

# STORAGE CHANNEL ID
STORAGE_CHANNEL_ID = -1003959246499

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    args = context.args

    # IF USER OPENED SHARE LINK
    if args:

        try:
            msg_id = int(args[0])

            # COPY FILE FROM STORAGE CHANNEL TO USER
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
        "Send me media to store."
    )


# SAVE MEDIA
async def save_media(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    # ONLY ADMIN CAN STORE FILES
    if user_id != ADMIN_ID:

        await update.message.reply_text(
            "You are not allowed."
        )

        return

    try:

        # COPY MESSAGE TO STORAGE CHANNEL
        stored_message = await context.bot.copy_message(
            chat_id=STORAGE_CHANNEL_ID,
            from_chat_id=update.effective_chat.id,
            message_id=update.message.message_id,
        )

        msg_id = stored_message.message_id

        bot_username = (
            await context.bot.get_me()
        ).username

        # GENERATE SHARE LINK
        share_link = (
            f"https://t.me/{bot_username}?start={msg_id}"
        )

        await update.message.reply_text(
            f"Stored Successfully ✅\n\n{share_link}"
        )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "Failed to store file."
        )


def main():

    # CREATE APPLICATION
    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    # COMMAND HANDLER
    app.add_handler(
        CommandHandler("start", start)
    )

    # MEDIA HANDLER
    app.add_handler(
        MessageHandler(
            filters.ALL & ~filters.COMMAND,
            save_media,
        )
    )

    print("Bot running...")

    # START BOT
    app.run_polling(
        drop_pending_updates=True
    )


if __name__ == "__main__":
    main()
