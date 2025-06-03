from telegram import Update
from telegram.ext import *
from handlers.admin_handler import *
from handlers.message_handler import *
from datetime import datetime
import sqlite3
import asyncio
from database import init_db

init_db()
import logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! 👋\n"
        "Send me your message, and I'll forward it to the admin for review."
    )

BOT_TOKEN = '8118183259:AAFPZvmFRhhE_t5MKM0ZpaAe0j1uSeBF1ME'

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Core handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message))
    
    # Admin handler (only approve/reject buttons)
    app.add_handler(CallbackQueryHandler(handle_admin_response))
    
    app.add_error_handler(error_handler)
    
    print("Bot is running...")
    app.run_polling()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error {context.error}")
    if update.message:
        await update.message.reply_text("⚠️ An error occurred. Please try again.")

if __name__ == "__main__":
    main()