#!/bin/bash

echo "🚀 Setting up ChatBot with LLM Integration..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo "📥 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✏️  Please edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY: Get from https://platform.openai.com/api-keys"
    echo "   - SLACK_BOT_TOKEN: Get from https://api.slack.com/apps (if using Slack)"
    echo "   - SLACK_SIGNING_SECRET: Get from https://api.slack.com/apps (if using Slack)"
fi

echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Run 'source venv/bin/activate' to activate the environment"
echo "3. Run 'python chatbot.py' for CLI mode"
echo "4. Run 'python slack_bot.py' for Slack integration"
echo ""
echo "🧠 For LLM features, you'll need an OpenAI API key"
echo "🔗 Get one at: https://platform.openai.com/api-keys"