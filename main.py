import logging
import re
import asyncio
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, CallbackQueryHandler, filters

import os

# Bot token from Telegram
TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in environment variables")

# List of abusive words (add more as needed)
ABUSIVE_WORDS = [
    'fuck', 'shit', 'damn', 'bitch', 'asshole', 'bastard', 'cunt', 'dick', 'pussy',
    'nigger', 'faggot', 'retard', 'whore', 'slut', 'crap', 'bullshit', 'suck',
    'dumbass', 'idiot', 'stupid', 'moron', 'jerk', 'prick', 'twat', 'wanker',
    'ጭቅቅታሙ', 'ውሻ', 'ጥንቡ', 'አህያ', 'ተበዳ', 'ሲበዳ', 'አይጥ', '💩', '🐀', '🐪', '🐫', 'ቂጥ', 'ፔሬድ', 'የወር አበባ',
    'ቁላ', 'ተኮላሸ', 'ፈርሴ', 'Netflix', 'ሽባ', 'ቀነዘረ', 'ጭገራም', 'tebeda', 'fara', 'ahya', 'qeshim', 'ems',
    'gim', 'ግም', 'tenb', 'tnb', 'ላም', 'ላሟ', 'lam', 'lemagn', 'ለማኝ', 'ዲቻ', 'ቆቦ',
    'ወሸላ', 'የለማኝ ልጅ', 'yelemagn lej', 'ሸርሙጣ', 'ቡሽጢ', 'ቡሽቲ', 'bushti', 'jezba', 'ጀዝባ', 'እከካም', 'እከክ', 'ekekam', 'ekek', 'tija', 'ጥጃ', 'ዝንጀሮ', 'zenjero',
    'ቡሌ', 'ሌስትሮ', 'ሊስትሮ', 'ቆሎ', 'ሸታታ', 'የሚሸት', 'ፋንድያ', 'qolo', 'shetata', 'yemishet', 'listro', 'entenh', 'እንትንህ', 'አይምሮህ', '🧠', 'denez', 'dengay', 'ደነዝ', 'ድንጋይ', 'tnbu', 'sedb', 'ስድብ', 'temar', 'ተማር', 'temr', 'ፓንት', 'አዟሪ', 'pant', 'azuari', 'beg', 'በግ', 'ግመል', 'camel', 'gemel', 'መሃይቡ', 'መሀይሙ', 'mehaymu', 'terfrafi', 'ትርፍራፊ', 'ከብት', 'kebt', 'ሽማግሌ', 'በክት', 'bekt', 'jel', 'ጅል', 'ላጭቼ', 'ላጭ', 'ቂንጥር', 'ቆለጥ', 'እንዳልቨዳ', 'ጭቅቅታም',
    'ሸሌ', 'ጭገር', 'ጥንብ', 'ሸተቱ', 'ቆሻሻ', 'እበት', 'ሹጢ', 'ደደብ', 'ተበጂ', 'ጡት', 'ኩበት', 'ጡቷ', 'wsha', 'ይከኩህ', 'ልደክለልሀ', 'ዲቻው', 'wusha', 'ይደክሉህ',
    'atbdada', 'jil', 'gimatatam'
]

def generate_fuzzy_pattern(word):
    """Generate a regex pattern that matches the word with repeated characters and optional '*' insertions."""
    return ''.join(f'{re.escape(c)}+?\\*?' for c in word)

ABUSIVE_PATTERNS = [generate_fuzzy_pattern(word) for word in ABUSIVE_WORDS]

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and delete if they contain abusive words."""
    logging.info(f"Received message update: {update}")
    if update.message and update.message.text:
        chat = update.message.chat
        logging.info(f"Message from chat {chat.id}, type: {chat.type}, text: '{update.message.text}'")
        # Only process messages in groups/supergroups
        if chat.type in ['group', 'supergroup']:
            text = update.message.text.lower()
            logging.info(f"Processing message in group/supergroup: '{text}'")
            # Check if any abusive pattern matches in the message
            matching_indices = [i for i, pattern in enumerate(ABUSIVE_PATTERNS) if re.search(pattern, text, re.IGNORECASE)]
            if matching_indices:
                matching_words = [ABUSIVE_WORDS[i] for i in matching_indices]
                logging.warning(f"Detected abusive message in chat {chat.id}, matching words: {matching_words}")
                try:
                    # Delete the message
                    await context.bot.delete_message(
                        chat_id=chat.id,
                        message_id=update.message.message_id
                    )
                    logging.warning(f"Successfully deleted abusive message in chat {chat.id}")
                except Exception as e:
                    logging.error(f"Failed to delete message in chat {chat.id}: {e}")
            else:
                logging.info(f"No abusive content detected in message: '{text}'")
        else:
            logging.info(f"Ignoring message from non-group chat: {chat.type}")
    else:
        logging.info("Received update without message or text")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message with interactive buttons when the /start command is issued."""
    keyboard = [
        [InlineKeyboardButton("Help", callback_data='help')],
        [InlineKeyboardButton("Add Word", callback_data='add_word')],
        [InlineKeyboardButton("Remove Word", callback_data='remove_word')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome to the Spam Filter Bot! I help keep chats clean by filtering abusive messages. Choose an option:", reply_markup=reply_markup)

if __name__ == '__main__':
    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add start command handler
    application.add_handler(CommandHandler("start", start))

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start dummy web server for Render
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import threading

    class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Bot is running")

    def run_health_check():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
        print(f"Health check server running on port {port}")
        server.serve_forever()

    # Start web server in background thread
    threading.Thread(target=run_health_check, daemon=True).start()

    # Start the bot
    application.run_polling()