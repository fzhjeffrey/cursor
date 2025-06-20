# ChatBot Project

A simple yet comprehensive Python chat bot implementation with conversation handling, intent recognition, and persistent conversation history.

## Features

- 🤖 **Interactive Chat Interface**: Command-line based chat interface
- 🧠 **Intent Recognition**: Recognizes common intents like greetings, goodbyes, questions
- 💾 **Conversation History**: Saves and manages conversation history
- 🎭 **Personality**: Friendly responses with some humor
- 📝 **Name Recognition**: Remembers user names during conversation
- 💬 **Extensible Responses**: Easy to add new response patterns

## Quick Start

### Basic Usage

```bash
python chatbot.py
```

### Programmatic Usage

```python
from chatbot import ChatBot

# Create a bot instance
bot = ChatBot("MyBot")

# Chat with the bot
response = bot.chat("Hello!")
print(response)  # "Hello! How can I help you today?"

# Get conversation history
history = bot.get_conversation_history()

# Save conversation
bot.save_conversation("my_chat.json")
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
├── chatbot.py          # Main chatbot implementation
├── requirements.txt    # Dependencies (standard library only)
├── README.md          # This file
└── a.py               # Original test file
```

## Class Structure

### ChatBot Class

#### Methods:
- `chat(message)`: Process a message and return a response
- `recognize_intent(message)`: Identify the intent behind a message
- `generate_response(message)`: Generate an appropriate response
- `get_conversation_history()`: Retrieve conversation history
- `save_conversation(filename)`: Save conversation to JSON file
- `clear_history()`: Clear conversation history

#### Attributes:
- `name`: Bot's name
- `conversation_history`: List of conversation entries
- `user_name`: Remembered user name
- `responses`: Dictionary of response patterns
- `patterns`: Dictionary of intent recognition patterns

## Example Conversation

```
🤖 ChatBot is ready! Type 'quit' to exit.

You: Hello!
Bot: Hi there! What's on your mind?

You: My name is Alice
Bot: Nice to meet you, Alice! How can I help you today?

You: Tell me a joke
Bot: Why don't scientists trust atoms? Because they make up everything!

You: What time is it?
Bot: The current time is 14:30:25

You: Thanks!
Bot: You're welcome!

You: quit
Bot: Goodbye, Alice! Have a wonderful day!
```

## Customization

### Adding New Intents

1. Add patterns to the `patterns` dictionary:
```python
self.patterns['new_intent'] = [r'\b(pattern1|pattern2)\b']
```

2. Add responses to the `responses` dictionary:
```python
self.responses['new_intent'] = ["Response 1", "Response 2"]
```

### Modifying Responses

Edit the `responses` dictionary in the `__init__` method to customize bot responses.

## Advanced Features

### Conversation Persistence

Conversations are automatically saved with timestamps and can be exported to JSON format.

### Name Recognition

The bot can extract and remember user names from natural language input.

### Extensible Architecture

The bot is designed to be easily extended with new intents, responses, and functionality.

## Contributing

Feel free to enhance the bot by:
- Adding new intent patterns
- Improving response variety
- Adding new features like sentiment analysis
- Implementing more sophisticated NLP capabilities

## License

This project is open source and available under the MIT License.