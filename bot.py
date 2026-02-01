import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from db import db
from cache import get_cache, set_cache

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

# ===== COMMANDS =====

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Cache check
    cached = await get_cache(f"user:{user.id}")
    if cached:
        await update.message.reply_text("Welcome back (cached) 🚀")
        return

    ref = None
    if context.args:
        try:
            ref = int(context.args[0])
        except:
            pass

    await db.add_user(user.id, user.username, ref)

    if ref and ref != user.id:
        await db.add_balance(ref, 1)

    await set_cache(f"user:{user.id}", "1")

    await update.message.reply_text(
        f"Hello {user.first_name} 👋\nReferral system active 🚀"
    )

async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await db.get_user(update.effective_user.id)

    if not user:
        await update.message.reply_text("Use /start first")
        return

    await update.message.reply_text(
        f"💰 Balance: {user['balance']} points\n"
        f"👥 Invites: {user['invites']}"
    )

# ===== INIT =====

async def post_init(app):
    await db.connect()
    await db.setup()
    print("✅ DB Connected")

if __name__ == "__main__":
    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))

    print("🚀 Bot Running...")
    app.run_polling()
