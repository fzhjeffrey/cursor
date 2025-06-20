import re
import random
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChatBot:
    def __init__(self, name: str = "Assistant", use_llm: bool = True):
        self.name = name
        self.conversation_history = []
        self.user_name = None
        self.use_llm = use_llm
        
        # Initialize OpenAI client if LLM is enabled
        self.openai_client = None
        if self.use_llm and os.environ.get("OPENAI_API_KEY"):
            try:
                self.openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
            except Exception as e:
                print(f"Warning: Could not initialize OpenAI client: {e}")
                self.openai_client = None
        
        # System prompt for the LLM
        self.system_prompt = f"""You are {self.name}, a friendly and helpful chat bot. 
        You should be conversational, engaging, and helpful. Keep responses concise but warm.
        If a user tells you their name, remember it and use it in future responses.
        You can answer questions, have conversations, tell jokes, and provide helpful information.
        Be natural and personable in your responses."""
        
        # Predefined responses for common patterns (fallback)
        self.responses = {
            'greeting': [
                "Hello! How can I help you today?",
                "Hi there! What's on your mind?",
                "Greetings! How are you doing?",
                "Hey! Nice to meet you!"
            ],
            'goodbye': [
                "Goodbye! Have a great day!",
                "See you later! Take care!",
                "Bye! It was nice chatting with you!",
                "Until next time! Stay safe!"
            ],
            'thanks': [
                "You're welcome!",
                "Happy to help!",
                "No problem at all!",
                "Glad I could assist!"
            ],
            'how_are_you': [
                "I'm doing well, thank you for asking!",
                "I'm great! How about you?",
                "I'm functioning perfectly! How are you?",
                "I'm having a wonderful day! Thanks for asking!"
            ],
            'name_question': [
                f"I'm {self.name}, your friendly chat bot!",
                f"You can call me {self.name}. What's your name?",
                f"I'm {self.name}! Nice to meet you!"
            ],
            'weather': [
                "I don't have access to real-time weather data, but I hope it's nice where you are!",
                "I can't check the weather right now, but you could try a weather app or website!",
                "Sorry, I don't have weather information, but I hope you're having good weather!"
            ],
            'time': [
                f"The current time is {datetime.now().strftime('%H:%M:%S')}",
                f"Right now it's {datetime.now().strftime('%I:%M %p')}",
                f"The time is {datetime.now().strftime('%H:%M')}"
            ],
            'joke': [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the scarecrow win an award? He was outstanding in his field!",
                "What do you call a fake noodle? An impasta!",
                "Why don't eggs tell jokes? They'd crack each other up!"
            ],
            'default': [
                "That's interesting! Can you tell me more?",
                "I see. What else is on your mind?",
                "Hmm, that's something to think about!",
                "Could you elaborate on that?",
                "I'm not sure I understand completely. Could you rephrase that?",
                "That's a good point. What do you think about it?"
            ]
        }
        
        # Patterns for intent recognition (fallback)
        self.patterns = {
            'greeting': [r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b'],
            'goodbye': [r'\b(bye|goodbye|see you|farewell|talk to you later|ttyl)\b'],
            'thanks': [r'\b(thanks|thank you|thx|appreciated)\b'],
            'how_are_you': [r'\b(how are you|how\'re you|how do you feel|how are things)\b'],
            'name_question': [r'\b(what\'s your name|who are you|what are you called|your name)\b'],
            'weather': [r'\b(weather|temperature|rain|sunny|cloudy|forecast)\b'],
            'time': [r'\b(time|what time|current time|clock)\b'],
            'joke': [r'\b(joke|funny|laugh|humor|humour|make me laugh)\b']
        }

    def get_user_name(self, message: str) -> Optional[str]:
        """Extract user name from message if provided"""
        name_patterns = [
            r"my name is (\w+)",
            r"i'm (\w+)",
            r"i am (\w+)",
            r"call me (\w+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message.lower())
            if match:
                return match.group(1).capitalize()
        return None

    def get_conversation_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history for LLM context"""
        return self.conversation_history[-limit:] if self.conversation_history else []

    def generate_llm_response(self, message: str) -> Optional[str]:
        """Generate response using OpenAI LLM"""
        if not self.openai_client:
            return None
        
        try:
            # Build conversation history for context
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add conversation history
            for conv in self.get_conversation_context():
                messages.append({"role": "user", "content": conv['user']})
                if conv['bot']:
                    messages.append({"role": "assistant", "content": conv['bot']})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Add user name context if known
            if self.user_name:
                messages.insert(1, {
                    "role": "system", 
                    "content": f"The user's name is {self.user_name}. Use their name naturally in conversation when appropriate."
                })
            
            # Call OpenAI API
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=150,
                temperature=0.7,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return None

    def recognize_intent(self, message: str) -> str:
        """Recognize the intent behind a user message"""
        message_lower = message.lower()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'default'

    def generate_fallback_response(self, message: str) -> str:
        """Generate fallback response using pattern matching"""
        # Check if user is providing their name
        potential_name = self.get_user_name(message)
        if potential_name:
            self.user_name = potential_name
            return f"Nice to meet you, {self.user_name}! How can I help you today?"
        
        # Recognize intent and generate response
        intent = self.recognize_intent(message)
        
        # Handle personalized responses
        if intent == 'greeting' and self.user_name:
            return f"Hello again, {self.user_name}! How can I assist you?"
        elif intent == 'goodbye' and self.user_name:
            return f"Goodbye, {self.user_name}! Have a wonderful day!"
        
        # Get random response from the appropriate category
        responses = self.responses.get(intent, self.responses['default'])
        return random.choice(responses)

    def generate_response(self, message: str) -> str:
        """Generate an appropriate response based on the message"""
        # Check if user is providing their name (handle this first regardless of LLM)
        potential_name = self.get_user_name(message)
        if potential_name:
            self.user_name = potential_name
        
        # Try LLM first if available
        if self.use_llm and self.openai_client:
            llm_response = self.generate_llm_response(message)
            if llm_response:
                return llm_response
        
        # Fall back to pattern-based responses
        return self.generate_fallback_response(message)

    def chat(self, message: str) -> str:
        """Main chat method that processes a message and returns a response"""
        if not message.strip():
            return "I didn't catch that. Could you say something?"
        
        # Store the conversation
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.conversation_history.append({
            'timestamp': timestamp,
            'user': message,
            'bot': None
        })
        
        # Generate response
        response = self.generate_response(message)
        
        # Update conversation history with bot response
        self.conversation_history[-1]['bot'] = response
        
        return response

    def get_conversation_history(self) -> List[Dict]:
        """Return the conversation history"""
        return self.conversation_history

    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation history to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'bot_name': self.name,
                'user_name': self.user_name,
                'conversation': self.conversation_history,
                'llm_enabled': self.use_llm and self.openai_client is not None
            }, f, indent=2)
        
        return filename

    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.user_name = None

    def get_status(self) -> Dict:
        """Get bot status information"""
        return {
            'name': self.name,
            'llm_enabled': self.use_llm and self.openai_client is not None,
            'conversations': len(self.conversation_history),
            'user_name': self.user_name
        }

def main():
    """Interactive chat session"""
    print("🤖 ChatBot is ready! Type 'quit' to exit.\n")
    
    # Check if OpenAI API key is available
    if os.environ.get("OPENAI_API_KEY"):
        print("🧠 LLM integration enabled with OpenAI GPT!")
        bot = ChatBot("ChatBot", use_llm=True)
    else:
        print("⚠️  No OpenAI API key found. Using pattern-based responses.")
        print("   Add OPENAI_API_KEY to your .env file to enable LLM features.")
        bot = ChatBot("ChatBot", use_llm=False)
    
    print(f"📊 Bot status: {bot.get_status()}\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print(f"Bot: {bot.generate_response('goodbye')}")
                
                # Ask if user wants to save conversation
                if bot.conversation_history:
                    save = input("\nWould you like to save this conversation? (y/n): ").strip().lower()
                    if save in ['y', 'yes']:
                        filename = bot.save_conversation()
                        print(f"Conversation saved to {filename}")
                
                break
            
            if user_input:
                response = bot.chat(user_input)
                print(f"Bot: {response}\n")
        
        except KeyboardInterrupt:
            print(f"\nBot: {bot.generate_response('goodbye')}")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()