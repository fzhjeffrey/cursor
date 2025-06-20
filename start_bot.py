#!/usr/bin/env python3
"""
Bot Starter Script
Choose between CLI chatbot or Slack bot
"""

import sys
import os
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import slack_bolt
        import flask
        import dotenv
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("Install with: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists for Slack bot"""
    if not Path('.env').exists():
        print("⚠️  No .env file found for Slack bot")
        print("Copy .env.example to .env and add your Slack tokens")
        return False
    
    # Load and check required vars
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET"]
    missing_vars = [var for var in required_vars if not os.environ.get(var) or os.environ.get(var) == f"your-{var.lower().replace('_', '-')}-here"]
    
    if missing_vars:
        print("❌ Missing or placeholder values in .env file:")
        for var in missing_vars:
            print(f"   - {var}")
        return False
    
    return True

def run_cli_bot():
    """Run the CLI chatbot"""
    print("🤖 Starting CLI ChatBot...")
    try:
        from chatbot import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error running CLI bot: {e}")

def run_slack_bot():
    """Run the Slack bot"""
    if not check_env_file():
        return
    
    print("🚀 Starting Slack ChatBot...")
    try:
        from slack_bot import main
        main()
    except KeyboardInterrupt:
        print("\n👋 Slack bot stopped!")
    except Exception as e:
        print(f"❌ Error running Slack bot: {e}")
        print("Check your .env file and Slack app configuration")

def main():
    """Main menu"""
    print("🤖 ChatBot Starter")
    print("==================")
    
    if not check_requirements():
        return
    
    print("\nChoose your bot:")
    print("1. CLI ChatBot (command line)")
    print("2. Slack ChatBot (Slack integration)")
    print("3. Exit")
    
    try:
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            run_cli_bot()
        elif choice == "2":
            run_slack_bot()
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")
            main()
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()