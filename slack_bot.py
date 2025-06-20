import os
import re
from typing import Dict, Any
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from dotenv import load_dotenv
from chatbot import ChatBot

# Load environment variables
load_dotenv()

class SlackChatBot:
    def __init__(self):
        # Initialize Slack app
        self.app = App(
            token=os.environ.get("SLACK_BOT_TOKEN"),
            signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
        )
        
        # Initialize Flask app for webhook handling
        self.flask_app = Flask(__name__)
        self.handler = SlackRequestHandler(self.app)
        
        # Store individual ChatBot instances per user
        self.user_bots: Dict[str, ChatBot] = {}
        
        # Set up event handlers
        self._setup_handlers()
        
        # Set up Flask routes
        self._setup_flask_routes()
    
    def _setup_handlers(self):
        """Set up Slack event handlers"""
        
        # Handle direct messages and mentions
        @self.app.message(re.compile(".*"))
        def handle_message(message, say, client):
            user_id = message['user']
            text = message['text']
            
            # Get or create a ChatBot instance for this user
            if user_id not in self.user_bots:
                self.user_bots[user_id] = ChatBot(f"SlackBot")
            
            user_bot = self.user_bots[user_id]
            
            # Generate response using the chatbot
            response = user_bot.chat(text)
            
            # Send response back to Slack
            say(response)
        
        # Handle app mentions (@botname)
        @self.app.event("app_mention")
        def handle_app_mention(event, say, client):
            user_id = event['user']
            text = event['text']
            
            # Remove the bot mention from the text
            text = re.sub(r'<@\w+>', '', text).strip()
            
            # Get or create a ChatBot instance for this user
            if user_id not in self.user_bots:
                self.user_bots[user_id] = ChatBot(f"SlackBot")
            
            user_bot = self.user_bots[user_id]
            
            # Generate response
            response = user_bot.chat(text)
            
            # Send response back to the channel
            say(response)
        
        # Handle the app_home_opened event
        @self.app.event("app_home_opened")
        def handle_app_home_opened(client, event):
            user_id = event["user"]
            
            # Create welcome message for App Home
            try:
                client.views_publish(
                    user_id=user_id,
                    view={
                        "type": "home",
                        "blocks": [
                            {
                                "type": "header",
                                "text": {
                                    "type": "plain_text",
                                    "text": "🤖 Welcome to SlackBot!"
                                }
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "*Hello!* I'm your friendly Slack chat bot. You can:\n\n• Send me direct messages\n• Mention me in channels with `@SlackBot`\n• Ask me questions, tell jokes, or just chat!\n\nI can recognize greetings, answer questions about time, tell jokes, and much more. Try saying hello!"
                                }
                            },
                            {
                                "type": "divider"
                            },
                            {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": "*Quick Examples:*\n• `Hello!`\n• `Tell me a joke`\n• `What time is it?`\n• `My name is [Your Name]`"
                                }
                            }
                        ]
                    }
                )
            except Exception as e:
                print(f"Error publishing home view: {e}")
        
        # Handle slash commands (optional)
        @self.app.command("/chat")
        def handle_chat_command(ack, respond, command):
            ack()
            user_id = command['user_id']
            text = command['text']
            
            # Get or create a ChatBot instance for this user
            if user_id not in self.user_bots:
                self.user_bots[user_id] = ChatBot(f"SlackBot")
            
            user_bot = self.user_bots[user_id]
            
            # Generate response
            response = user_bot.chat(text)
            
            respond(f"🤖 {response}")
    
    def _setup_flask_routes(self):
        """Set up Flask routes for Slack events"""
        
        @self.flask_app.route("/slack/events", methods=["POST"])
        def slack_events():
            return self.handler.handle(request)
        
        @self.flask_app.route("/health", methods=["GET"])
        def health_check():
            return {"status": "healthy", "bot": "SlackBot is running!"}, 200
        
        @self.flask_app.route("/", methods=["GET"])
        def home():
            return {
                "message": "SlackBot is running!",
                "endpoints": {
                    "events": "/slack/events",
                    "health": "/health"
                }
            }, 200
    
    def run(self, host="0.0.0.0", port=3000, debug=False):
        """Run the Flask app"""
        print(f"🤖 SlackBot is starting on {host}:{port}")
        print(f"📡 Webhook URL: http://{host}:{port}/slack/events")
        print(f"❤️  Health check: http://{host}:{port}/health")
        
        self.flask_app.run(host=host, port=port, debug=debug)

def main():
    """Main entry point"""
    # Check for required environment variables
    required_vars = ["SLACK_BOT_TOKEN", "SLACK_SIGNING_SECRET"]
    missing_vars = [var for var in required_vars if not os.environ.get(var)]
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease check your .env file or environment variables.")
        return
    
    # Create and run the bot
    slack_bot = SlackChatBot()
    
    # Get port from environment or use default
    port = int(os.environ.get("PORT", 3000))
    host = os.environ.get("HOST", "0.0.0.0")
    debug = os.environ.get("DEBUG", "false").lower() == "true"
    
    slack_bot.run(host=host, port=port, debug=debug)

if __name__ == "__main__":
    main()