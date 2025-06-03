# admin_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3

from handlers.message_handler import ADMIN_CHAT_ID

# Your target channels
CHANNEL_IDS = ["@randomniggachannel"] #change with ur actual channel username

def get_db_connection():
    return sqlite3.connect('bot_database.db')

async def handle_admin_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, message_id = query.data.split(":")
    message_id = int(message_id)

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get message from database
    cursor.execute("SELECT user_id, text, status FROM messages WHERE id = ?", (message_id,))
    message_data = cursor.fetchone()
    
    if not message_data:
        await query.edit_message_text("⚠️ Message no longer available.")
        conn.close()
        return
    
    user_id, message_text, status = message_data

    if action == "approve":
        # Update status in database
        cursor.execute("UPDATE messages SET status = 'approved' WHERE id = ?", (message_id,))
        conn.commit()
        
        # Send to all channels immediately
        for channel in CHANNEL_IDS:
            await post_to_channel(context, message_text, channel)
        
        # Notify user
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="🎉 Your message has been approved and posted to the channel!"
            )
        except Exception as e:
            print(f"Could not notify user {user_id}: {e}")
        
        await query.edit_message_text("✅ Approved and posted to channels.")
    
    elif action == "reject":
        # Update status in database
        cursor.execute("UPDATE messages SET status = 'rejected' WHERE id = ?", (message_id,))
        conn.commit()
        
        # Notify user
        try:
            await context.bot.send_message(
                chat_id=user_id,
                text="❌ Your message has been rejected by the admin."
            )
        except Exception as e:
            print(f"Could not notify user {user_id}: {e}")
        
        await query.edit_message_text("❌ Message rejected.")
    
    conn.close()

async def post_to_channel(context, message_text, channel_id):
    formatted_message = f"""👋hear me Out:

{message_text}

Don't forget to share {channel_id}"""
    
    await context.bot.send_message(
        chat_id=channel_id,
        text=formatted_message
    )