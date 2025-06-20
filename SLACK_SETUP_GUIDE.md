# Slack Bot Setup Guide

This guide will walk you through setting up your Slack chat bot from scratch.

## Prerequisites

- Python 3.7 or higher
- A Slack workspace where you can create apps
- A server or local machine to run the bot

## Step 1: Create a Slack App

1. Go to [https://api.slack.com/apps](https://api.slack.com/apps)
2. Click **"Create New App"**
3. Choose **"From scratch"**
4. Enter an app name (e.g., "ChatBot")
5. Select your Slack workspace
6. Click **"Create App"**

## Step 2: Configure Bot Permissions

1. In your app settings, go to **"OAuth & Permissions"**
2. Scroll down to **"Scopes"** and add these Bot Token Scopes:
   - `app_mentions:read` - View messages that directly mention your bot
   - `channels:history` - View messages and content in public channels
   - `chat:write` - Send messages as the bot
   - `im:history` - View messages in direct messages
   - `im:read` - View basic information about direct messages
   - `im:write` - Start direct messages with people

3. Click **"Install to Workspace"**
4. Copy the **"Bot User OAuth Token"** (starts with `xoxb-`)

## Step 3: Get Your Signing Secret

1. Go to **"Basic Information"** in your app settings
2. Scroll down to **"App Credentials"**
3. Copy the **"Signing Secret"**

## Step 4: Set Up Event Subscriptions

1. Go to **"Event Subscriptions"**
2. Turn on **"Enable Events"**
3. Set the **Request URL** to: `https://your-server.com/slack/events`
   - For local testing with ngrok: `https://your-ngrok-url.ngrok.io/slack/events`
4. Subscribe to these bot events:
   - `app_mention` - When your bot is mentioned
   - `message.im` - Messages in direct message channels
   - `app_home_opened` - When a user opens your app's Home tab

5. Click **"Save Changes"**

## Step 5: Enable App Home (Optional)

1. Go to **"App Home"**
2. Enable **"Home Tab"**
3. Check **"Allow users to send Slash commands and messages from the messages tab"**

## Step 6: Create Slash Command (Optional)

1. Go to **"Slash Commands"**
2. Click **"Create New Command"**
3. Set:
   - **Command**: `/chat`
   - **Request URL**: `https://your-server.com/slack/events`
   - **Short Description**: `Chat with the bot`
   - **Usage Hint**: `[your message]`

## Step 7: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 8: Configure Environment Variables

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your tokens:
   ```
   SLACK_BOT_TOKEN=xoxb-your-actual-bot-token
   SLACK_SIGNING_SECRET=your-actual-signing-secret
   ```

## Step 9: Run the Bot

### For Production
```bash
python slack_bot.py
```

### For Development with Auto-reload
```bash
DEBUG=true python slack_bot.py
```

## Step 10: Test Your Bot

1. **Direct Message**: Send a DM to your bot
2. **Channel Mention**: Type `@YourBotName hello` in a channel
3. **Slash Command**: Type `/chat hello there` (if you set up the slash command)
4. **App Home**: Click on your bot's name and visit the Home tab

## Local Development with ngrok

If you're developing locally, you'll need to expose your local server to the internet:

1. Install ngrok: [https://ngrok.com/](https://ngrok.com/)
2. Run your bot: `python slack_bot.py`
3. In another terminal: `ngrok http 3000`
4. Copy the HTTPS URL from ngrok (e.g., `https://abc123.ngrok.io`)
5. Update your Slack app's Request URLs to use this ngrok URL

## Deployment Options

### Heroku
1. Create a `Procfile`:
   ```
   web: python slack_bot.py
   ```
2. Set environment variables in Heroku dashboard
3. Deploy your app

### Docker
1. Create a `Dockerfile`:
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   EXPOSE 3000
   CMD ["python", "slack_bot.py"]
   ```

### AWS/GCP/Azure
Deploy using your preferred cloud platform's container or app service.

## Troubleshooting

### Common Issues

1. **"url_verification" error**: Make sure your Request URL is correct and your server is running
2. **"invalid_auth" error**: Check your bot token and signing secret
3. **Bot not responding**: Verify your bot has the necessary OAuth scopes
4. **Events not received**: Ensure your server is publicly accessible

### Debug Mode

Run with debug mode to see detailed logs:
```bash
DEBUG=true python slack_bot.py
```

### Health Check

Visit `http://your-server:3000/health` to verify your bot is running.

## Security Notes

- Never commit your `.env` file to version control
- Keep your bot token and signing secret secure
- Use HTTPS in production
- Regularly rotate your tokens if compromised

## Support

If you encounter issues:
1. Check the Slack API documentation: [https://api.slack.com/](https://api.slack.com/)
2. Review your app's Event Subscriptions logs in the Slack app dashboard
3. Check your server logs for error messages

Happy chatting! 🤖