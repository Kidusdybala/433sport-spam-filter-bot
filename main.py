import logging
import re
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Bot token from Telegram
TOKEN = '8363894608:AAHZCyI_dWP4OtMxLP-w1claLf8P6G1G5JQ'

# List of abusive words (add more as needed)
ABUSIVE_WORDS = [
    'fuck', 'shit', 'damn', 'bitch', 'asshole', 'bastard', 'cunt', 'dick', 'pussy',
    'nigger', 'faggot', 'retard', 'whore', 'slut', 'crap', 'bullshit', 'suck',
    'dumbass', 'idiot', 'stupid', 'moron', 'jerk', 'prick', 'twat', 'wanker',
    'ጭቅቅታሙ', 'ውሻ', 'ጥንቡ', 'አህያ', 'ተበዳ', 'ሲበዳ', 'አይጥ', '💩', '🐀', '🐪', '🐫', 'ቂጥ', 'ፔሬድ', 'የወር አበባ',
    'ቁላ', 'ተኮላሸ', 'ፈርሴ', 'Netflix', 'ሽባ', 'ቀነዘረ', 'ጭገራም', 'tebeda', 'fara', 'ahya', 'qeshim', 'ems',
    'gm', 'gim', 'ግም', 'tenb', 'tnb', 'ላም', 'ላሟ', 'lam', 'lemagn', 'ለማኝ', 'ዲቻ', 'ቆቦ',
    'ወሸላ', 'የለማኝ ልጅ', 'yelemagn lej', 'ሸርሙጣ', 'ቡሽጢ', 'ቡሽቲ', 'bushti', 'jezba', 'ጀዝባ', 'እከካም', 'እከክ', 'ekekam', 'ekek', 'tija', 'ጥጃ', 'ዝንጀሮ', 'zenjero',
    'ቡሌ', 'ሌስትሮ', 'ሊስትሮ', 'ቆሎ', 'ሸታታ', 'የሚሸት', 'ፋንድያ', 'qolo', 'shetata', 'yemishet', 'listro', 'entenh', 'እንትንህ', 'አይምሮህ', '🧠', 'denez', 'dengay', 'ደነዝ', 'ድንጋይ', 'tnbu', 'sedb', 'ስድብ', 'temar', 'ተማር', 'temr', 'ፓንት', 'አዟሪ', 'pant', 'azuari', 'beg', 'በግ', 'ግመል', 'camel', 'gemel', 'መሃይቡ', 'መሀይሙ', 'mehaymu', 'terfrafi', 'ትርፍራፊ', 'ከብት', 'kebt', 'ሽማግሌ', 'በክት', 'bekt', 'jel', 'ጅል', 'ላጭቼ', 'ላጭ', 'ቂንጥር', 'ቆለጥ', 'እንዳልቨዳ', 'ጭቅቅታም'
]

def generate_fuzzy_pattern(word):
    """Generate a regex pattern that matches the word with repeated characters."""
    return ''.join(f'{re.escape(c)}+?' for c in word)

ABUSIVE_PATTERNS = [generate_fuzzy_pattern(word) for word in ABUSIVE_WORDS]

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages and delete if they contain abusive words."""
    if update.message and update.message.text:
        chat = update.message.chat
        # Only process messages in groups/supergroups
        if chat.type in ['group', 'supergroup']:
            text = update.message.text.lower()
            # Check if any abusive pattern matches in the message
            if any(re.search(pattern, text, re.IGNORECASE) for pattern in ABUSIVE_PATTERNS):
                try:
                    # Delete the message
                    await context.bot.delete_message(
                        chat_id=chat.id,
                        message_id=update.message.message_id
                    )
                    logging.info(f"Deleted abusive message in chat {chat.id}")
                except Exception as e:
                    logging.error(f"Failed to delete message: {e}")

if __name__ == '__main__':
    # Build the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Add message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    application.run_polling()