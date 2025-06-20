# ChatBot Project 🤖

A comprehensive Python chat bot implementation with both command-line interface and **Slack integration**! Chat with your bot directly in Slack channels or via direct messages.

## Features

- 🤖 **Interactive Chat Interface**: Command-line based chat interface
- 💬 **Slack Integration**: Full Slack bot with DMs, mentions, and slash commands
- 🧠 **Intent Recognition**: Recognizes common intents like greetings, goodbyes, questions
- 💾 **Conversation History**: Saves and manages conversation history per user
- 🎭 **Personality**: Friendly responses with humor and personality
- 📝 **Name Recognition**: Remembers user names during conversation
- 🏠 **App Home**: Beautiful Slack App Home with welcome message
- 💬 **Extensible Responses**: Easy to add new response patterns

## Quick Start

### Slack Bot (Recommended)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Slack app** (detailed guide in [SLACK_SETUP_GUIDE.md](SLACK_SETUP_GUIDE.md)):
   - Create a Slack app at [https://api.slack.com/apps](https://api.slack.com/apps)
   - Get your bot token and signing secret
   - Configure OAuth scopes and event subscriptions

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your Slack tokens
   ```

4. **Run the Slack bot:**
   ```bash
   python slack_bot.py
   ```

5. **Chat with your bot in Slack!**
   - Send direct messages
   - Mention `@YourBot` in channels
   - Use `/chat` slash command (if configured)

### CLI Bot (Original)

```bash
python chatbot.py
```

## Usage Examples

### In Slack
- **Direct Message**: Just message your bot directly
- **Channel Mention**: `@ChatBot tell me a joke`
- **Slash Command**: `/chat what time is it?`

### Command Line
```
🤖 ChatBot is ready! Type 'quit' to exit.

You: Hello!
Bot: Hi there! What's on your mind?

You: My name is Alice
Bot: Nice to meet you, Alice! How can I help you today?
```

## Supported Intents

The bot can recognize and respond to:

- **Greetings**: "hi", "hello", "hey", "good morning"
- **Goodbyes**: "bye", "goodbye", "see you later"  
- **Thanks**: "thanks", "thank you"
- **How are you**: "how are you", "how are things"
- **Name questions**: "what's your name", "who are you"
- **Weather**: "weather", "rain", "sunny"
- **Time**: "what time", "current time"
- **Jokes**: "tell me a joke", "make me laugh"

## File Structure

```
.
├── slack_bot.py           # 🆕 Main Slack bot implementation
├── chatbot.py            # Original CLI chatbot class
├── requirements.txt      # Dependencies (including Slack SDK)
├── .env.example         # 🆕 Environment configuration template
├── SLACK_SETUP_GUIDE.md # 🆕 Detailed Slack setup instructions
├── README.md            # This file
└── a.py                 # Original test file
```

## Architecture

### SlackChatBot Class (New!)
- Integrates with Slack's Events API and Socket Mode
- Handles direct messages, mentions, and slash commands
- Maintains separate ChatBot instances per user
- Provides App Home interface

### ChatBot Class (Original)
- Core conversation logic and intent recognition
- Conversation history management
- Extensible response patterns
- Name recognition and personalization

## Slack Features

- **Direct Messages**: Private 1:1 conversations
- **Channel Mentions**: Respond when mentioned in channels
- **App Home**: Beautiful welcome interface
- **Slash Commands**: `/chat` command integration
- **Multi-User**: Separate conversation history per user
- **Real-time**: Instant responses via webhooks

## Configuration

### Environment Variables

```bash
# Required for Slack integration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# Optional server settings
PORT=3000
HOST=0.0.0.0
DEBUG=false
```

### Slack App Permissions

Required Bot Token Scopes:
- `app_mentions:read` - Respond to mentions
- `chat:write` - Send messages
- `im:history` - Read direct messages
- `im:read` - Access DM info
- `im:write` - Send direct messages

## Development

### Local Development
1. Use [ngrok](https://ngrok.com/) to expose your local server
2. Run: `ngrok http 3000`
3. Update your Slack app's Request URL to the ngrok HTTPS URL

### Debug Mode
```bash
DEBUG=true python slack_bot.py
```

### Health Check
Visit `http://localhost:3000/health` to verify the bot is running.

## Deployment

### Heroku
```bash
# Create Procfile
echo "web: python slack_bot.py" > Procfile

# Set environment variables in Heroku dashboard
# Deploy your app
```

### Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ["python", "slack_bot.py"]
```

## Customization

### Adding New Intents

1. Add patterns to the `patterns` dictionary in `chatbot.py`:
```python
self.patterns['new_intent'] = [r'\b(pattern1|pattern2)\b']
```

2. Add responses to the `responses` dictionary:
```python
self.responses['new_intent'] = ["Response 1", "Response 2"]
```

### Modifying Slack Behavior

Edit the event handlers in `slack_bot.py` to customize:
- Message processing logic
- Response formatting
- App Home content
- Slash command behavior

## API Endpoints

When running the Slack bot:
- `POST /slack/events` - Slack event webhook
- `GET /health` - Health check endpoint
- `GET /` - Basic info endpoint

## Troubleshooting

### Common Issues
1. **Bot not responding**: Check OAuth scopes and event subscriptions
2. **"url_verification" error**: Ensure your server is publicly accessible
3. **"invalid_auth" error**: Verify your bot token and signing secret

### Debug Steps
1. Check server logs with `DEBUG=true`
2. Verify your Slack app configuration
3. Test the health endpoint
4. Review Slack app Event Subscriptions logs

## Contributing

Enhance the bot by:
- Adding new conversation patterns
- Improving Slack UI components
- Implementing advanced NLP features
- Adding integrations with external APIs
- Creating custom slash commands

## License

This project is open source and available under the MIT License.

---

**Ready to chat?** Follow the [Slack Setup Guide](SLACK_SETUP_GUIDE.md) to get your bot running in Slack! 🚀