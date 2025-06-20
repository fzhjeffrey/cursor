# ChatBot Project 🤖

A comprehensive Python chat bot implementation with both command-line interface, **Slack integration**, and **LLM (GPT) integration**! Chat with your bot directly in Slack channels, via direct messages, or command line - now powered by OpenAI's GPT for intelligent responses.

## ✨ New Features

- � **LLM Integration**: Now powered by OpenAI's GPT-3.5-turbo for intelligent responses
- 🔄 **Hybrid Response System**: Uses LLM by default, falls back to pattern-based responses
- 📝 **Conversation Context**: Maintains conversation history for contextual responses
- ⚙️ **Easy Setup**: Automated setup script for quick deployment
- 🔧 **Flexible Configuration**: Enable/disable LLM features via environment variables

## Features

- �🤖 **Interactive Chat Interface**: Command-line based chat interface
- 💬 **Slack Integration**: Full Slack bot with DMs, mentions, and slash commands
- 🧠 **LLM-Powered Responses**: Uses OpenAI GPT for natural conversations
- 🔄 **Fallback System**: Pattern-based responses when LLM is unavailable
- 💾 **Conversation History**: Saves and manages conversation history per user
- 🎭 **Personality**: Friendly responses with humor and personality
- 📝 **Name Recognition**: Remembers user names during conversation
- 🏠 **App Home**: Beautiful Slack App Home with welcome message
- 💬 **Extensible Responses**: Easy to add new response patterns

## Quick Start

### 🚀 Automated Setup (Recommended)

1. **Run the setup script:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Configure your API keys:**
   ```bash
   nano .env  # Edit the .env file with your API keys
   ```

3. **Add your OpenAI API key** (get one at [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)):
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

4. **Run the bot:**
   ```bash
   source venv/bin/activate
   python chatbot.py        # For CLI mode
   python slack_bot.py      # For Slack integration
   ```

### Manual Setup

1. **Install system dependencies:**
   ```bash
   sudo apt update && sudo apt install -y python3.13-venv python3-pip
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

### Slack Bot Setup

For Slack integration, follow the detailed guide in [SLACK_SETUP_GUIDE.md](SLACK_SETUP_GUIDE.md).

## Usage Examples

### CLI with LLM
```
🧠 LLM integration enabled with OpenAI GPT!
📊 Bot status: {'name': 'ChatBot', 'llm_enabled': True, 'conversations': 0, 'user_name': None}

You: Hello! I'm working on a Python project and need some help.
Bot: Hello! I'd be happy to help you with your Python project. What specific aspect are you working on or what challenges are you facing? Whether it's debugging, design patterns, libraries, or anything else Python-related, I'm here to assist!

You: My name is Alice
Bot: Nice to meet you, Alice! It's great to know who I'm chatting with. Now, what can I help you with regarding your Python project?
```

### In Slack
- **Direct Message**: Just message your bot directly
- **Channel Mention**: `@ChatBot can you help me understand async programming in Python?`
- **Slash Command**: `/chat what's the weather like?`

### Fallback Mode (No API Key)
```
⚠️  No OpenAI API key found. Using pattern-based responses.
📊 Bot status: {'name': 'ChatBot', 'llm_enabled': False, 'conversations': 0, 'user_name': None}

You: Hello!
Bot: Hi there! What's on your mind?
```

## Configuration

### Environment Variables

```bash
# Required for LLM features
OPENAI_API_KEY=sk-your-openai-api-key

# Required for Slack integration
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_SIGNING_SECRET=your-signing-secret

# Optional server settings
PORT=3000
HOST=0.0.0.0
DEBUG=false
```

### LLM Settings

The bot uses GPT-3.5-turbo with these default settings:
- **Max tokens**: 150 (for concise responses)
- **Temperature**: 0.7 (balanced creativity/consistency)
- **Context window**: Last 10 conversation turns

You can modify these in the `generate_llm_response()` method in `chatbot.py`.

## Supported Intents

### LLM Mode (Primary)
- **Natural conversations**: Ask anything, get intelligent responses
- **Context awareness**: References previous conversation
- **Technical help**: Programming, explanations, advice
- **Creative tasks**: Writing, jokes, stories
- **Personalization**: Uses your name and adapts to your style

### Fallback Mode (Pattern-based)
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
├── setup.sh             # 🆕 Automated setup script
├── .env.example         # 🆕 Environment configuration template
├── slack_bot.py         # Main Slack bot implementation
├── chatbot.py           # 🔄 Enhanced ChatBot class with LLM integration
├── requirements.txt     # 🔄 Updated dependencies (includes OpenAI)
├── SLACK_SETUP_GUIDE.md # Detailed Slack setup instructions
├── README.md            # This file
└── venv/               # 🆕 Virtual environment (created by setup)
```

## Architecture

### Enhanced ChatBot Class
- **LLM Integration**: Uses OpenAI GPT-3.5-turbo for responses
- **Hybrid System**: Falls back to pattern matching if LLM fails
- **Context Management**: Maintains conversation history for context
- **Flexible Configuration**: Can disable LLM features
- **Error Handling**: Graceful fallback when API is unavailable

### SlackChatBot Class
- Integrates with Slack's Events API and Socket Mode
- Creates individual ChatBot instances per user
- Maintains separate conversation history per user
- Provides App Home interface

## API Integration

### OpenAI Integration
- Uses the official OpenAI Python library
- Implements conversation context management
- Includes error handling and fallback logic
- Configurable model parameters (temperature, max_tokens)

### Conversation Flow
1. User sends message
2. Bot checks for name extraction
3. If LLM enabled and API key available:
   - Builds conversation context
   - Calls OpenAI API
   - Returns LLM response
4. If LLM fails or disabled:
   - Falls back to pattern matching
   - Returns predefined response

## Development

### Testing LLM Integration
```bash
# Test with LLM enabled
OPENAI_API_KEY=your-key python chatbot.py

# Test fallback mode
python chatbot.py  # (without API key)
```

### Adding Custom Intents
1. Add patterns to `patterns` dictionary in `chatbot.py`
2. Add responses to `responses` dictionary
3. LLM will handle most cases automatically

### Monitoring Usage
- Bot saves LLM status in conversation files
- Check `get_status()` method for current configuration
- Monitor OpenAI API usage in their dashboard

## Deployment

### Local Development
1. Run `./setup.sh`
2. Configure `.env` file
3. Test with `python chatbot.py`

### Production Deployment
- Set environment variables in your hosting platform
- Use `requirements.txt` for dependency management
- Consider API rate limits and costs for OpenAI usage

### Cost Considerations
- GPT-3.5-turbo costs approximately $0.002 per 1K tokens
- 150 token responses ≈ $0.0003 per message
- Monitor usage in OpenAI dashboard
- Consider implementing usage limits for production

## Troubleshooting

### LLM Issues
- **"No OpenAI API key found"**: Add `OPENAI_API_KEY` to `.env`
- **API errors**: Check API key validity and OpenAI service status
- **Slow responses**: Consider reducing `max_tokens` or using faster models
- **High costs**: Monitor usage and implement rate limiting

### Setup Issues
- **Virtual environment errors**: Ensure `python3.13-venv` is installed
- **Permission denied**: Use `sudo` for system package installation
- **Import errors**: Activate virtual environment with `source venv/bin/activate`

## License

This project is open source and available under the MIT License.

---

**Ready to chat with AI?** Run `./setup.sh` to get started with LLM-powered conversations! 🧠✨