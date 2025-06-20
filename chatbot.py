import re
import random
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from openai import OpenAI
from dotenv import load_dotenv
from atlassian import Confluence
from bs4 import BeautifulSoup
import requests

# Load environment variables
load_dotenv()

class ConfluenceBot:
    def __init__(self, name: str = "ConfluenceBot", use_llm: bool = True):
        self.name = name
        self.conversation_history = []
        self.user_name = None
        self.use_llm = use_llm
        self.confluence_content_cache = {}
        
        # Initialize DeepSeek client (OpenAI-compatible)
        self.deepseek_client = None
        if self.use_llm and os.environ.get("DEEPSEEK_API_KEY"):
            try:
                self.deepseek_client = OpenAI(
                    api_key=os.environ.get("DEEPSEEK_API_KEY"),
                    base_url="https://api.deepseek.com"
                )
            except Exception as e:
                print(f"Warning: Could not initialize DeepSeek client: {e}")
                self.deepseek_client = None
        
        # Initialize Confluence client
        self.confluence = None
        if os.environ.get("CONFLUENCE_URL") and os.environ.get("CONFLUENCE_USERNAME"):
            try:
                self.confluence = Confluence(
                    url=os.environ.get("CONFLUENCE_URL"),
                    username=os.environ.get("CONFLUENCE_USERNAME"),
                    password=os.environ.get("CONFLUENCE_PASSWORD"),  # or API token
                    api_version="cloud"  # or "server" for on-premise
                )
            except Exception as e:
                print(f"Warning: Could not initialize Confluence client: {e}")
                self.confluence = None
        
        # Enhanced system prompt for Confluence Q&A
        self.system_prompt = f"""You are {self.name}, an intelligent assistant that specializes in helping users with information from Confluence pages.

Your capabilities include:
1. Answering questions about specific Confluence pages and their content
2. Summarizing Confluence documentation
3. Finding relevant information across multiple pages
4. General conversation and assistance

When answering questions about Confluence content:
- Always reference the specific page title and provide accurate information from the content
- If you don't have access to the requested Confluence page, clearly state this
- Provide detailed and helpful answers based on the available content
- If asked about something not in the Confluence content, clearly distinguish between general knowledge and specific documentation

Be conversational, helpful, and accurate. Remember user names and maintain context across the conversation."""
        
        # Predefined responses for common patterns (fallback)
        self.responses = {
            'greeting': [
                "Hello! I can help you with Confluence pages and general questions. What would you like to know?",
                "Hi there! I'm here to help with your Confluence documentation and more. How can I assist?",
                "Greetings! I can answer questions about your Confluence pages. What's on your mind?",
                "Hey! I'm your Confluence assistant. What can I help you with today?"
            ],
            'goodbye': [
                "Goodbye! Feel free to ask me about Confluence pages anytime!",
                "See you later! I'm here whenever you need help with documentation!",
                "Bye! It was great helping you with your Confluence questions!",
                "Until next time! Don't hesitate to ask about your documentation!"
            ],
            'thanks': [
                "You're welcome! Happy to help with your Confluence needs!",
                "Glad I could assist with your documentation questions!",
                "No problem! I'm here for all your Confluence queries!",
                "You're welcome! Always ready to help with your content!"
            ],
            'confluence_help': [
                "I can help you with Confluence pages! Try asking me to load a page by title or ID, or ask questions about loaded content.",
                "You can ask me to read Confluence pages and answer questions about them. What page would you like me to look at?",
                "I'm designed to work with Confluence documentation. Would you like me to load a specific page?"
            ],
            'default': [
                "That's interesting! Can you tell me more, or would you like me to check a Confluence page?",
                "I see. Is there a specific Confluence page I should look at to help answer that?",
                "Could you clarify what you're looking for? I can search Confluence content if that helps!",
                "I'm here to help! Would you like me to look up information in your Confluence space?"
            ]
        }
        
        # Patterns for intent recognition
        self.patterns = {
            'greeting': [r'\b(hi|hello|hey|greetings|good morning|good afternoon|good evening)\b'],
            'goodbye': [r'\b(bye|goodbye|see you|farewell|talk to you later|ttyl)\b'],
            'thanks': [r'\b(thanks|thank you|thx|appreciated)\b'],
            'confluence_help': [r'\b(confluence|page|document|docs|documentation)\b'],
            'load_page': [r'\b(load|get|fetch|read|show me|open)\s.*(page|document)\b'],
            'search_confluence': [r'\b(search|find|look for)\b.*\b(confluence|page|docs)\b']
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

    def fetch_confluence_page_by_title(self, space_key: str, page_title: str) -> Optional[Dict]:
        """Fetch a Confluence page by space key and title"""
        if not self.confluence:
            return None
        
        try:
            page = self.confluence.get_page_by_title(space_key, page_title, expand='body.storage')
            if page:
                # Extract and clean the content
                content = self.extract_text_from_confluence_html(page['body']['storage']['value'])
                
                # Safe URL construction
                confluence_url = os.environ.get('CONFLUENCE_URL', '')
                page_url = f"{confluence_url}{page['_links']['webui']}" if confluence_url else page['_links']['webui']
                
                page_data = {
                    'id': page['id'],
                    'title': page['title'],
                    'content': content,
                    'space_key': space_key,
                    'url': page_url
                }
                
                # Cache the content
                cache_key = f"{space_key}:{page_title}"
                self.confluence_content_cache[cache_key] = page_data
                
                return page_data
        except Exception as e:
            print(f"Error fetching Confluence page: {e}")
            return None

    def fetch_confluence_page_by_id(self, page_id: str) -> Optional[Dict]:
        """Fetch a Confluence page by ID"""
        if not self.confluence:
            return None
        
        try:
            page = self.confluence.get_page_by_id(page_id, expand='body.storage,space')
            if page:
                content = self.extract_text_from_confluence_html(page['body']['storage']['value'])
                
                # Safe URL construction
                confluence_url = os.environ.get('CONFLUENCE_URL', '')
                page_url = f"{confluence_url}{page['_links']['webui']}" if confluence_url else page['_links']['webui']
                
                page_data = {
                    'id': page['id'],
                    'title': page['title'],
                    'content': content,
                    'space_key': page['space']['key'],
                    'url': page_url
                }
                
                # Cache the content
                cache_key = f"id:{page_id}"
                self.confluence_content_cache[cache_key] = page_data
                
                return page_data
        except Exception as e:
            print(f"Error fetching Confluence page by ID: {e}")
            return None

    def search_confluence_pages(self, query: str, space_key: str = None) -> List[Dict]:
        """Search for Confluence pages"""
        if not self.confluence:
            return []
        
        try:
            # Build CQL query
            cql = f'text ~ "{query}"'
            if space_key:
                cql += f' and space = "{space_key}"'
            
            results = self.confluence.cql(cql, limit=5)
            pages = []
            
            # Safe URL construction
            confluence_url = os.environ.get('CONFLUENCE_URL', '')
            
            for result in results.get('results', []):
                if result.get('content', {}).get('type') == 'page':
                    webui_link = result['content'].get('_links', {}).get('webui', '')
                    page_url = f"{confluence_url}{webui_link}" if confluence_url else webui_link
                    
                    page_info = {
                        'id': result['content']['id'],
                        'title': result['content']['title'],
                        'space_key': result['content']['space']['key'],
                        'url': page_url
                    }
                    pages.append(page_info)
            
            return pages
        except Exception as e:
            print(f"Error searching Confluence: {e}")
            return []

    def extract_text_from_confluence_html(self, html_content: str) -> str:
        """Extract clean text from Confluence HTML content"""
        if not html_content:
            return ""
        
        try:
            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text and clean up
            text = soup.get_text()
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text
        except Exception as e:
            print(f"Error extracting text from HTML: {e}")
            return html_content  # Return raw content if parsing fails

    def get_confluence_context(self, message: str) -> str:
        """Get relevant Confluence content for the current message"""
        context_parts = []
        
        # Check if user is asking about a specific page
        page_mention = self.extract_page_reference(message)
        if page_mention:
            page_data = self.load_page_from_reference(page_mention)
            if page_data:
                context_parts.append(f"Page: {page_data['title']}")
                context_parts.append(f"Content: {page_data['content'][:2000]}...")
        
        # Include recently loaded pages
        for cache_key, page_data in list(self.confluence_content_cache.items())[-3:]:
            if len(context_parts) < 3:  # Limit context size
                context_parts.append(f"Available Page: {page_data['title']}")
                context_parts.append(f"Content snippet: {page_data['content'][:500]}...")
        
        return "\n\n".join(context_parts)

    def extract_page_reference(self, message: str) -> Optional[str]:
        """Extract page reference from user message"""
        # Look for patterns like "page titled X", "load page X", etc.
        patterns = [
            r'(?:page|document)(?:\s+titled?|\s+called?|\s+named?)?\s+"([^"]+)"',
            r'(?:page|document)(?:\s+titled?|\s+called?|\s+named?)?\s+([A-Z][A-Za-z\s]+)',
            r'(?:load|get|fetch|read|show)\s+(?:page\s+)?(?:titled?\s+)?(?:called?\s+)?([A-Z][A-Za-z\s]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return None

    def load_page_from_reference(self, page_reference: str) -> Optional[Dict]:
        """Load a page from a reference (title or ID)"""
        # Try as page ID first (if it's numeric)
        if page_reference.isdigit():
            return self.fetch_confluence_page_by_id(page_reference)
        
        # Try to find by title in different spaces
        common_spaces = os.environ.get("CONFLUENCE_SPACES", "").split(",")
        
        for space_key in common_spaces:
            if space_key.strip():
                page_data = self.fetch_confluence_page_by_title(space_key.strip(), page_reference)
                if page_data:
                    return page_data
        
        return None

    def generate_deepseek_response(self, message: str) -> Optional[str]:
        """Generate response using DeepSeek LLM"""
        if not self.deepseek_client:
            return None
        
        try:
            # Get Confluence context
            confluence_context = self.get_confluence_context(message)
            
            # Build conversation history
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # Add Confluence context if available
            if confluence_context:
                messages.append({
                    "role": "system", 
                    "content": f"Relevant Confluence Content:\n{confluence_context}"
                })
            
            # Add conversation history
            for conv in self.get_conversation_context():
                messages.append({"role": "user", "content": conv['user']})
                if conv['bot']:
                    messages.append({"role": "assistant", "content": conv['bot']})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Add user name context if known
            if self.user_name:
                messages.insert(-1, {
                    "role": "system", 
                    "content": f"The user's name is {self.user_name}. Use their name naturally when appropriate."
                })
            
            # Call DeepSeek API
            response = self.deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                max_tokens=500,
                temperature=0.7,
                stream=False
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Error generating DeepSeek response: {e}")
            return None

    def get_conversation_context(self, limit: int = 10) -> List[Dict]:
        """Get recent conversation history for LLM context"""
        return self.conversation_history[-limit:] if self.conversation_history else []

    def recognize_intent(self, message: str) -> str:
        """Recognize the intent behind a user message"""
        message_lower = message.lower()
        
        for intent, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    return intent
        
        return 'default'

    def handle_confluence_command(self, message: str) -> Optional[str]:
        """Handle specific Confluence commands"""
        message_lower = message.lower()
        
        # Load page command
        if "load page" in message_lower or "read page" in message_lower:
            page_ref = self.extract_page_reference(message)
            if page_ref:
                page_data = self.load_page_from_reference(page_ref)
                if page_data:
                    return f"✅ Successfully loaded page: **{page_data['title']}**\n\nYou can now ask me questions about this page content!"
                else:
                    return f"❌ Could not find page: '{page_ref}'. Please check the title and try again."
        
        # Search command
        if "search" in message_lower and ("confluence" in message_lower or "pages" in message_lower):
            # Extract search query
            search_match = re.search(r'search\s+(?:for\s+)?(?:confluence\s+)?(?:pages?\s+)?(?:about\s+)?(.+)', message_lower)
            if search_match:
                query = search_match.group(1).strip()
                results = self.search_confluence_pages(query)
                if results:
                    result_list = "\n".join([f"• {r['title']} (ID: {r['id']})" for r in results[:5]])
                    return f"🔍 Found {len(results)} pages for '{query}':\n\n{result_list}\n\nWould you like me to load any of these pages?"
                else:
                    return f"🔍 No pages found for '{query}'. Try different keywords."
        
        return None

    def generate_fallback_response(self, message: str) -> str:
        """Generate fallback response using pattern matching"""
        # Check if user is providing their name
        potential_name = self.get_user_name(message)
        if potential_name:
            self.user_name = potential_name
            return f"Nice to meet you, {self.user_name}! I can help you with Confluence pages and answer questions about your documentation. What would you like to know?"
        
        # Handle Confluence commands
        confluence_response = self.handle_confluence_command(message)
        if confluence_response:
            return confluence_response
        
        # Recognize intent and generate response
        intent = self.recognize_intent(message)
        
        # Handle personalized responses
        if intent == 'greeting' and self.user_name:
            return f"Hello again, {self.user_name}! Ready to help with your Confluence questions!"
        elif intent == 'goodbye' and self.user_name:
            return f"Goodbye, {self.user_name}! Come back anytime for Confluence help!"
        
        # Get random response from the appropriate category
        responses = self.responses.get(intent, self.responses['default'])
        return random.choice(responses)

    def generate_response(self, message: str) -> str:
        """Generate an appropriate response based on the message"""
        # Check if user is providing their name (handle this first regardless of LLM)
        potential_name = self.get_user_name(message)
        if potential_name:
            self.user_name = potential_name
        
        # Handle page loading automatically if page reference is detected
        page_ref = self.extract_page_reference(message)
        if page_ref and page_ref not in [p.get('title', '') for p in self.confluence_content_cache.values()]:
            page_data = self.load_page_from_reference(page_ref)
            if page_data:
                # Let the LLM know we loaded the page
                message += f" (I've loaded the page '{page_data['title']}' for context)"
        
        # Try DeepSeek first if available
        if self.use_llm and self.deepseek_client:
            llm_response = self.generate_deepseek_response(message)
            if llm_response:
                return llm_response
        
        # Fall back to pattern-based responses
        return self.generate_fallback_response(message)

    def chat(self, message: str) -> str:
        """Main chat method that processes a message and returns a response"""
        if not message.strip():
            return "I didn't catch that. Could you say something? You can ask me about Confluence pages!"
        
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

    def get_loaded_pages(self) -> List[str]:
        """Get list of currently loaded page titles"""
        return [page_data['title'] for page_data in self.confluence_content_cache.values()]

    def clear_confluence_cache(self):
        """Clear the Confluence content cache"""
        self.confluence_content_cache = {}

    def get_status(self) -> Dict:
        """Get bot status information"""
        return {
            'name': self.name,
            'deepseek_enabled': self.use_llm and self.deepseek_client is not None,
            'confluence_enabled': self.confluence is not None,
            'conversations': len(self.conversation_history),
            'loaded_pages': len(self.confluence_content_cache),
            'user_name': self.user_name
        }

    def save_conversation(self, filename: Optional[str] = None):
        """Save conversation history to a JSON file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"confluence_bot_conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump({
                'bot_name': self.name,
                'user_name': self.user_name,
                'conversation': self.conversation_history,
                'loaded_pages': list(self.confluence_content_cache.keys()),
                'deepseek_enabled': self.use_llm and self.deepseek_client is not None,
                'confluence_enabled': self.confluence is not None
            }, f, indent=2)
        
        return filename

    def clear_history(self):
        """Clear the conversation history"""
        self.conversation_history = []
        self.user_name = None

# Backwards compatibility
ChatBot = ConfluenceBot

def main():
    """Interactive chat session"""
    print("🤖 ConfluenceBot is ready! Type 'quit' to exit.\n")
    
    # Check configurations
    deepseek_enabled = bool(os.environ.get("DEEPSEEK_API_KEY"))
    confluence_enabled = bool(os.environ.get("CONFLUENCE_URL") and os.environ.get("CONFLUENCE_USERNAME"))
    
    if deepseek_enabled:
        print("🧠 DeepSeek integration enabled!")
    else:
        print("⚠️  No DeepSeek API key found. Add DEEPSEEK_API_KEY to your .env file.")
    
    if confluence_enabled:
        print("📚 Confluence integration enabled!")
    else:
        print("⚠️  Confluence not configured. Add CONFLUENCE_URL, CONFLUENCE_USERNAME, and CONFLUENCE_PASSWORD to your .env file.")
    
    bot = ConfluenceBot("ConfluenceBot", use_llm=deepseek_enabled)
    print(f"📊 Bot status: {bot.get_status()}\n")
    
    print("💡 Try asking:")
    print("  • 'Load page Project Overview'")
    print("  • 'What does the API documentation say about authentication?'")
    print("  • 'Search confluence pages about deployment'\n")
    
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