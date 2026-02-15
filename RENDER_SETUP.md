# Keeping Your Bot Active on Render Free Tier

Render's free tier puts services to sleep after 15 minutes of inactivity. This guide shows you how to keep your bot awake 24/7 using external monitoring services.

## How It Works

1. **Keep-Alive Server**: Your bot runs a Flask web server that responds to HTTP requests
2. **External Pinger**: A free monitoring service pings your bot every 5-14 minutes
3. **Result**: Render thinks your service is active and doesn't put it to sleep

## Setup Instructions

### Step 1: Deploy to Render

1. Push your code to GitHub
2. Connect your repository to Render
3. Add environment variable: `TELEGRAM_TOKEN=your_token_here`
4. Deploy the service
5. Note your service URL (e.g., `https://your-bot-name.onrender.com`)

### Step 2: Set Up UptimeRobot (Recommended - Free)

**UptimeRobot** is a free service that will ping your bot every 5 minutes.

1. Go to [UptimeRobot.com](https://uptimerobot.com/)
2. Create a free account
3. Click **"Add New Monitor"**
4. Configure:
   - **Monitor Type**: HTTP(s)
   - **Friendly Name**: 433 Sport Bot
   - **URL**: `https://your-bot-name.onrender.com/health`
   - **Monitoring Interval**: 5 minutes
5. Click **"Create Monitor"**

✅ Done! Your bot will now stay awake 24/7.

### Alternative Options

#### Option 2: Cron-Job.org

1. Go to [Cron-Job.org](https://cron-job.org/)
2. Create a free account
3. Create a new cron job:
   - **URL**: `https://your-bot-name.onrender.com/health`
   - **Interval**: Every 5 minutes
   - **Title**: Telegram Bot Keep-Alive

#### Option 3: Freshping by Freshworks

1. Go to [Freshping.io](https://www.freshping.io/)
2. Sign up for free
3. Add a new check:
   - **URL**: `https://your-bot-name.onrender.com/health`
   - **Check Interval**: 1 minute (free tier allows this)

#### Option 4: Self-Hosted Ping (Advanced)

If you have another always-on server, you can set up a cron job:

```bash
# Add to crontab (crontab -e)
*/5 * * * * curl https://your-bot-name.onrender.com/health
```

## Verification

### Check if Keep-Alive is Working

1. **Visit your bot URL** in a browser:
   ```
   https://your-bot-name.onrender.com/
   ```
   You should see: "Bot is alive and running!"

2. **Check the health endpoint**:
   ```
   https://your-bot-name.onrender.com/health
   ```
   You should see: `{"status": "healthy", "service": "telegram-bot"}`

3. **Monitor Render logs**:
   - Go to your Render dashboard
   - Click on your service
   - Check the "Logs" tab
   - You should see: "Keep-alive server started on port 10000"

### Test the Bot

1. Add the bot to a Telegram group
2. Make it an admin with "Delete messages" permission
3. Send a message with a filtered word
4. The bot should delete it immediately

## Troubleshooting

### Bot Still Sleeping

**Problem**: Bot goes to sleep despite UptimeRobot pinging

**Solutions**:
- Verify UptimeRobot is actually pinging (check their dashboard)
- Make sure the URL is correct (include `/health`)
- Check Render logs for incoming requests
- Reduce ping interval to 5 minutes (minimum for free tier)

### Health Check Failing

**Problem**: UptimeRobot shows "Down" status

**Solutions**:
- Check if your Render service is running
- Verify the `PORT` environment variable is set correctly
- Check Render logs for errors
- Test the URL manually in a browser

### Bot Not Responding to Messages

**Problem**: Bot is awake but not filtering messages

**Solutions**:
- Verify `TELEGRAM_TOKEN` is set correctly
- Check bot has admin permissions in the group
- Review Render logs for errors
- Test with `/start` command in private chat

## Cost Considerations

### Free Tier Limits

**Render Free Tier:**
- 750 hours/month of runtime (enough for 24/7 with one service)
- Sleeps after 15 minutes of inactivity (solved with keep-alive)
- 512 MB RAM
- Shared CPU

**UptimeRobot Free Tier:**
- 50 monitors
- 5-minute check intervals
- Unlimited checks

### When to Upgrade

Consider upgrading if:
- You need guaranteed uptime (99.9% SLA)
- You have multiple bots (free tier = 750 hours total)
- You need faster response times
- You want to avoid the initial wake-up delay

**Render Starter Plan**: $7/month
- No sleeping
- Faster CPU
- More RAM

## Best Practices

1. **Monitor Your Bot**: Use UptimeRobot's alert feature to get notified if the bot goes down
2. **Check Logs Regularly**: Review Render logs for errors or unusual activity
3. **Update Dependencies**: Keep `python-telegram-bot` and other packages updated
4. **Backup Your Token**: Store your `TELEGRAM_TOKEN` securely (password manager)
5. **Test After Deployment**: Always test the bot after deploying changes

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [UptimeRobot Documentation](https://uptimerobot.com/help/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

**Note**: The keep-alive method is a workaround for Render's free tier limitations. For production use with guaranteed uptime, consider upgrading to a paid plan.
