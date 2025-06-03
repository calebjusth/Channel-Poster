# message_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3

ADMIN_CHAT_ID = 5742309678  # Your admin chat ID replace with urs

def get_db_connection():
    return sqlite3.connect('bot_database.db')

async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message_text = update.message.text

    if user.id == ADMIN_CHAT_ID:
        return

    # Save message to database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO messages (user_id, text, status) VALUES (?, ?, ?)",
        (user.id, message_text, 'pending')
    )
    message_id = cursor.lastrowid
    conn.commit()
    conn.close()

    # Send message to admin with inline buttons
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve", callback_data=f"approve:{message_id}"),
            InlineKeyboardButton("❌ Reject", callback_data=f"reject:{message_id}")
        ]
    ])

    await context.bot.send_message(
        chat_id=ADMIN_CHAT_ID,
        text=f"📨 New message from {user.full_name} (ID: {user.id}):\n\n{message_text}",
        reply_markup=keyboard
    )

    await update.message.reply_text(
        "✅ Message sent to admin for review. " 
        "You'll be notified when it's published."
    )