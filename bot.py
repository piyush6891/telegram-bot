import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working!")

def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))

    # Railway webhook setup
    PORT = int(os.environ.get("PORT", 8080))
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL,
        webhook_path="/webhook"
    )

if __name__ == "__main__":
    main()