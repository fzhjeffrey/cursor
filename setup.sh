#!/bin/bash

# ConfluenceBot Setup Script
# Automated setup for ConfluenceBot with DeepSeek and Confluence integration

set -e

echo "🤖 ConfluenceBot Setup Script"
echo "============================="
echo

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.8 or later and try again."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "✅ Python $PYTHON_VERSION detected"

# Create virtual environment
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "� Activating virtual environment..."
source venv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# Upgrade pip
echo "� Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo
    echo "🔧 IMPORTANT: Please edit .env file with your credentials:"
    echo "   - Add your DeepSeek API key"
    echo "   - Configure Confluence connection details"
    echo "   - Optionally set up Slack integration"
else
    echo "✅ .env file already exists"
fi

echo
echo "🧪 Testing imports..."

# Test if all required packages can be imported
python3 -c "
import sys
try:
    import openai
    print('✅ OpenAI SDK (for DeepSeek)')
except ImportError as e:
    print('❌ OpenAI SDK import failed:', e)
    sys.exit(1)

try:
    from atlassian import Confluence
    print('✅ Atlassian Python API')
except ImportError as e:
    print('❌ Atlassian Python API import failed:', e)
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    print('✅ BeautifulSoup4')
except ImportError as e:
    print('❌ BeautifulSoup4 import failed:', e)
    sys.exit(1)

try:
    import lxml
    print('✅ lxml')
except ImportError as e:
    print('❌ lxml import failed:', e)
    sys.exit(1)

print('✅ All dependencies imported successfully!')
" || {
    echo "❌ Dependency import test failed"
    exit 1
}

echo
echo "🎉 Setup completed successfully!"
echo
echo "📋 Next steps:"
echo "1. Edit .env file with your credentials:"
echo "   nano .env  # or use your preferred editor"
echo
echo "2. Get your DeepSeek API key:"
echo "   https://platform.deepseek.com/api_keys"
echo
echo "3. Configure Confluence access:"
echo "   - For Cloud: Create API token at https://id.atlassian.com/manage-profile/security/api-tokens"
echo "   - For Server: Use your username and password"
echo
echo "4. Test the bot:"
echo "   source venv/bin/activate"
echo "   python chatbot.py"
echo
echo "5. For Slack integration:"
echo "   python slack_bot.py"
echo
echo "📚 Documentation:"
echo "   - Read LLM_INTEGRATION_SUMMARY.md for detailed information"
echo "   - Check README.md for usage examples"
echo
echo "� Happy chatting with your ConfluenceBot!"