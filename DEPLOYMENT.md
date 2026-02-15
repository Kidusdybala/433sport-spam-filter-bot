# PythonAnywhere Deployment Guide

This guide will walk you through deploying the 433 Sport Spam Filter Bot on PythonAnywhere.

## Prerequisites

1. A PythonAnywhere account (free tier works fine)
2. Your Telegram Bot Token from [@BotFather](https://t.me/botfather)
3. Git repository access (optional, for easier updates)

## Step-by-Step Deployment

### 1. Create a PythonAnywhere Account

- Go to [PythonAnywhere](https://www.pythonanywhere.com/)
- Sign up for a free account (Beginner tier is sufficient)

### 2. Upload Your Code

**Option A: Using Git (Recommended)**
```bash
# In PythonAnywhere Bash console
cd ~
git clone https://github.com/Kidusdybala/433sport-spam-filter-bot.git
cd 433sport-spam-filter-bot
```

**Option B: Manual Upload**
- Use the "Files" tab in PythonAnywhere
- Upload `main_pythonanywhere.py`, `requirements.txt`, and other files
- Create a directory like `/home/yourusername/spamfilter433_bot/`

### 3. Install Dependencies

Open a Bash console in PythonAnywhere:

```bash
cd ~/spamfilter433_bot  # or your project directory
pip3.10 install --user -r requirements.txt
```

> **Note**: PythonAnywhere free tier uses Python 3.10 by default. Adjust if needed.

### 4. Set Environment Variables

Create a `.env` file or set environment variables:

```bash
# Option 1: Create .env file (not recommended for production)
nano .env
# Add: TELEGRAM_TOKEN=your_actual_token_here

# Option 2: Set in bash profile (recommended)
echo 'export TELEGRAM_TOKEN="your_actual_token_here"' >> ~/.bashrc
source ~/.bashrc
```

### 5. Test the Bot Locally

```bash
python3.10 main_pythonanywhere.py
```

You should see "Bot is starting..." and the bot should respond to messages in your Telegram groups.

Press `Ctrl+C` to stop the test.

### 6. Run Bot as Always-On Task

PythonAnywhere free tier doesn't support always-on tasks, but you have options:

**Option A: Scheduled Task (Free Tier)**
- Go to "Tasks" tab
- Add a scheduled task to run every hour:
  ```bash
  cd /home/yourusername/spamfilter433_bot && python3.10 main_pythonanywhere.py
  ```
- **Limitation**: Bot will restart every hour, not truly always-on

**Option B: Upgrade to Paid Plan**
- Upgrade to a paid PythonAnywhere plan ($5/month)
- Go to "Consoles" tab
- Start a new console and run:
  ```bash
  cd ~/spamfilter433_bot
  python3.10 main_pythonanywhere.py
  ```
- The console will keep running as long as you don't close it

**Option C: Use Screen/Tmux (Recommended for Paid Plans)**
```bash
# Install screen
pip3.10 install --user screen

# Start a screen session
screen -S telegram_bot

# Run the bot
cd ~/spamfilter433_bot
python3.10 main_pythonanywhere.py

# Detach from screen: Press Ctrl+A, then D
# Reattach later: screen -r telegram_bot
```

### 7. Monitor the Bot

Check logs and status:

```bash
# View running processes
ps aux | grep python

# Check if bot is responding in Telegram
# Send a test message in your group
```

## Alternative: Using systemd (For Paid Plans with SSH)

If you have SSH access on a paid plan:

1. Create a systemd service file:
```bash
nano ~/.config/systemd/user/telegram-bot.service
```

2. Add this content:
```ini
[Unit]
Description=Telegram Spam Filter Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/yourusername/spamfilter433_bot
Environment="TELEGRAM_TOKEN=your_token_here"
ExecStart=/usr/bin/python3.10 /home/yourusername/spamfilter433_bot/main_pythonanywhere.py
Restart=always
RestartSec=10

[Install]
WantedBy=default.target
```

3. Enable and start:
```bash
systemctl --user enable telegram-bot
systemctl --user start telegram-bot
systemctl --user status telegram-bot
```

## Updating the Bot

```bash
cd ~/spamfilter433_bot
git pull origin main  # if using git
# Or re-upload files manually

# Restart the bot (method depends on how you're running it)
```

## Troubleshooting

### Bot Not Responding
- Check if the process is running: `ps aux | grep python`
- Verify environment variable: `echo $TELEGRAM_TOKEN`
- Check logs in the console output

### Import Errors
- Ensure dependencies are installed: `pip3.10 install --user -r requirements.txt`
- Check Python version: `python3.10 --version`

### Permission Errors
- Make sure you're in the correct directory
- Use `--user` flag when installing packages

### Bot Keeps Stopping
- Free tier limitations: Consider upgrading
- Use screen/tmux to keep sessions alive
- Check for errors in the console output

## Security Best Practices

1. **Never commit your `.env` file or token to Git**
   ```bash
   echo ".env" >> .gitignore
   ```

2. **Use environment variables instead of hardcoding tokens**

3. **Regularly update dependencies**
   ```bash
   pip3.10 install --user --upgrade -r requirements.txt
   ```

4. **Monitor bot activity and logs**

## Cost Considerations

- **Free Tier**: Limited to scheduled tasks (bot restarts hourly)
- **Hacker Plan ($5/month)**: Always-on consoles, more CPU time
- **Web Developer Plan ($12/month)**: More resources, better for production

## Support

For issues specific to:
- **PythonAnywhere**: Check their [help pages](https://help.pythonanywhere.com/)
- **Bot Code**: Open an issue on the GitHub repository
- **Telegram Bot API**: See [official documentation](https://core.telegram.org/bots/api)

---

**Note**: This bot uses polling mode which is perfect for PythonAnywhere. Webhook mode would require a web app setup which is more complex on PythonAnywhere's free tier.
