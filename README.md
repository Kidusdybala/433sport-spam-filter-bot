# 433 Sport Spam Filter Bot

A Telegram bot that automatically filters and removes abusive messages from group chats. Supports multiple languages including English and Amharic.

## Features

- 🛡️ **Automatic Spam Filtering**: Detects and removes messages containing abusive words
- 🌍 **Multi-language Support**: Filters content in English, Amharic, and emoji-based abuse
- 🔍 **Fuzzy Matching**: Catches variations with repeated characters (e.g., "f**k", "fuuuck")
- ⚡ **Real-time Processing**: Instant message deletion in group chats
- 🤖 **Easy Setup**: Simple configuration with environment variables
- 🔄 **Always Active**: Keep-alive system for 24/7 operation on free tier

## Quick Start

### Prerequisites

- Python 3.10 or higher
- A Telegram Bot Token from [@BotFather](https://t.me/botfather)

### Local Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kidusdybala/433sport-spam-filter-bot.git
   cd 433sport-spam-filter-bot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your token
   TELEGRAM_TOKEN=your_bot_token_here
   ```

4. **Run the bot**
   ```bash
   # For Render deployment (with keep-alive)
   python main.py
   
   # For PythonAnywhere
   python main_pythonanywhere.py
   ```

## Deployment

### Render (Recommended for 24/7 Free Hosting)

The bot includes keep-alive functionality to prevent Render's free tier from sleeping.

1. **Deploy to Render**:
   - Connect your GitHub repository to Render
   - Add `TELEGRAM_TOKEN` environment variable
   - Deploy automatically

2. **Set up UptimeRobot** (keeps bot awake):
   - Sign up at [UptimeRobot.com](https://uptimerobot.com/)
   - Add monitor: `https://your-bot-name.onrender.com/health`
   - Set interval: 5 minutes

📖 **See [RENDER_SETUP.md](RENDER_SETUP.md) for detailed instructions**

### PythonAnywhere (Alternative)

See the detailed [DEPLOYMENT.md](DEPLOYMENT.md) guide for step-by-step instructions.

**Quick summary:**
1. Upload code to PythonAnywhere
2. Install dependencies: `pip3.10 install --user -r requirements.txt`
3. Set environment variable: `export TELEGRAM_TOKEN="your_token"`
4. Run: `python3.10 main_pythonanywhere.py`

## Bot Setup in Telegram

1. **Create a bot** with [@BotFather](https://t.me/botfather)
   - Send `/newbot`
   - Follow the prompts to name your bot
   - Save the token provided

2. **Add bot to your group**
   - Add the bot as a group member
   - Make the bot an administrator with "Delete messages" permission

3. **Test the bot**
   - Send a test message with filtered words
   - The bot should automatically delete it

## Configuration

### Environment Variables

- `TELEGRAM_TOKEN` (required): Your bot token from BotFather
- `ENVIRONMENT` (optional): Set to `production` or `development`
- `PORT` (auto-set by Render): Port for the keep-alive web server

### Customizing Filtered Words

Edit the `ABUSIVE_WORDS` list in `main.py` or `main_pythonanywhere.py`:

```python
ABUSIVE_WORDS = [
    'word1', 'word2', 'word3',
    # Add your custom words here
]
```

## File Structure

```
spamfilter433_bot/
├── main.py                    # Main bot file (with keep-alive for Render)
├── main_pythonanywhere.py     # PythonAnywhere-optimized version
├── keep_alive.py             # Flask server for keep-alive functionality
├── requirements.txt           # Python dependencies
├── render.yaml               # Render deployment config
├── test.py                   # Testing script
├── .env.example              # Environment variables template
├── .gitignore               # Git ignore rules
├── DEPLOYMENT.md            # PythonAnywhere deployment guide
├── RENDER_SETUP.md          # Render keep-alive setup guide
└── README.md                # This file
```

## How It Works

### Message Filtering
1. **Message Detection**: Bot monitors all messages in groups where it's added
2. **Pattern Matching**: Uses regex patterns to detect abusive words (including variations)
3. **Automatic Deletion**: Removes messages containing filtered content
4. **Logging**: Records all actions for monitoring and debugging

### Keep-Alive System (Render)
1. **Flask Server**: Runs a lightweight web server on the PORT specified by Render
2. **Health Endpoint**: Provides `/health` endpoint for monitoring
3. **External Pinger**: UptimeRobot pings the bot every 5 minutes
4. **Result**: Bot stays active 24/7 on Render's free tier

## Troubleshooting

### Bot not responding
- Verify the bot token is correct
- Check if bot has admin permissions in the group
- Ensure the bot is running (check logs)

### Messages not being deleted
- Confirm bot has "Delete messages" permission
- Check if the word is in the `ABUSIVE_WORDS` list
- Review logs for error messages

### Bot sleeping on Render
- Set up UptimeRobot monitoring (see [RENDER_SETUP.md](RENDER_SETUP.md))
- Verify the health endpoint is accessible
- Check Render logs for incoming ping requests

### Deployment issues
- See [DEPLOYMENT.md](DEPLOYMENT.md) or [RENDER_SETUP.md](RENDER_SETUP.md)
- Check Python version compatibility (3.10+ required)
- Verify all dependencies are installed

## Development

### Running Tests

```bash
python test.py
```

### Adding New Features

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security

- **Never commit your `.env` file** - it contains sensitive tokens
- **Use environment variables** for all secrets
- **Regularly update dependencies** to patch security vulnerabilities
- **Monitor bot activity** for unusual behavior

## License

This project is open source and available under the MIT License.

## Support

- **Issues**: Open an issue on GitHub
- **Questions**: Contact the repository maintainer
- **Telegram Bot API**: [Official Documentation](https://core.telegram.org/bots/api)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Note**: This bot is designed for educational and community moderation purposes. Use responsibly and in accordance with Telegram's Terms of Service.
