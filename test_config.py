#!/usr/bin/env python3
"""
ConfluenceBot Configuration Test Script

This script helps validate your DeepSeek and Confluence configuration
before running the full chatbot.
"""

import os
import sys
from dotenv import load_dotenv

def test_imports():
    """Test if all required packages can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import openai
        print("✅ OpenAI SDK (for DeepSeek)")
    except ImportError as e:
        print(f"❌ OpenAI SDK import failed: {e}")
        return False
    
    try:
        from atlassian import Confluence
        print("✅ Atlassian Python API")
    except ImportError as e:
        print(f"❌ Atlassian Python API import failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✅ BeautifulSoup4")
    except ImportError as e:
        print(f"❌ BeautifulSoup4 import failed: {e}")
        return False
    
    try:
        import lxml
        print("✅ lxml")
    except ImportError as e:
        print(f"❌ lxml import failed: {e}")
        return False
    
    print("✅ All imports successful!\n")
    return True

def test_deepseek_config():
    """Test DeepSeek API configuration."""
    print("🧠 Testing DeepSeek configuration...")
    
    api_key = os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        print("❌ DEEPSEEK_API_KEY not found in environment")
        print("   Add it to your .env file")
        return False
    
    if api_key == "your_deepseek_api_key_here":
        print("❌ DEEPSEEK_API_KEY is still the default placeholder")
        print("   Replace it with your actual API key")
        return False
    
    print("✅ DeepSeek API key found")
    
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        
        # Test API call
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": "Hello, this is a test message."}],
            max_tokens=50
        )
        
        print("✅ DeepSeek API connection successful!")
        print(f"   Response: {response.choices[0].message.content.strip()[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ DeepSeek API test failed: {e}")
        return False

def test_confluence_config():
    """Test Confluence API configuration."""
    print("\n📚 Testing Confluence configuration...")
    
    url = os.environ.get("CONFLUENCE_URL")
    username = os.environ.get("CONFLUENCE_USERNAME")
    password = os.environ.get("CONFLUENCE_PASSWORD")
    
    if not url:
        print("❌ CONFLUENCE_URL not found in environment")
        return False
    
    if not username:
        print("❌ CONFLUENCE_USERNAME not found in environment")
        return False
    
    if not password:
        print("❌ CONFLUENCE_PASSWORD not found in environment")
        return False
    
    if any(val.startswith("your_") for val in [url, username, password] if val):
        print("❌ Some Confluence settings are still placeholders")
        print("   Update them with your actual credentials")
        return False
    
    print("✅ Confluence credentials found")
    
    try:
        from atlassian import Confluence
        
        # Determine API version
        api_version = "cloud" if url and "atlassian.net" in url else "server"
        
        confluence = Confluence(
            url=url,
            username=username,
            password=password,
            api_version=api_version
        )
        
        # Test API call - get current user info
        user_info = confluence.get_current_user()
        print(f"✅ Confluence API connection successful!")
        print(f"   Connected as: {user_info.get('displayName', username)}")
        
        # Test space access
        spaces = confluence.get_all_spaces(limit=5)
        if spaces.get('results'):
            print(f"   Accessible spaces: {len(spaces['results'])}")
            for space in spaces['results'][:3]:
                print(f"     - {space['name']} ({space['key']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Confluence API test failed: {e}")
        return False

def test_confluence_spaces():
    """Test configured Confluence spaces."""
    print("\n🔍 Testing Confluence spaces configuration...")
    
    spaces_config = os.environ.get("CONFLUENCE_SPACES", "")
    if not spaces_config:
        print("⚠️  No CONFLUENCE_SPACES configured - will search all accessible spaces")
        return True
    
    spaces = [s.strip() for s in spaces_config.split(",") if s.strip()]
    print(f"✅ Configured spaces: {', '.join(spaces)}")
    
    try:
        from atlassian import Confluence
        
        url = os.environ.get("CONFLUENCE_URL")
        username = os.environ.get("CONFLUENCE_USERNAME")
        password = os.environ.get("CONFLUENCE_PASSWORD")
        api_version = "cloud" if url and "atlassian.net" in url else "server"
        
        confluence = Confluence(
            url=url,
            username=username,
            password=password,
            api_version=api_version
        )
        
        # Test each configured space
        for space_key in spaces:
            try:
                space_info = confluence.get_space(space_key)
                print(f"   ✅ {space_key}: {space_info['name']}")
            except Exception as e:
                print(f"   ❌ {space_key}: Not accessible - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Space validation failed: {e}")
        return False

def main():
    """Main test function."""
    print("🤖 ConfluenceBot Configuration Test")
    print("==================================\n")
    
    # Load environment variables
    if os.path.exists('.env'):
        load_dotenv()
        print("✅ Loaded .env file\n")
    else:
        print("⚠️  No .env file found - using system environment variables\n")
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_deepseek_config()
    all_tests_passed &= test_confluence_config()
    all_tests_passed &= test_confluence_spaces()
    
    print("\n" + "="*50)
    if all_tests_passed:
        print("🎉 All tests passed! Your ConfluenceBot is ready to use.")
        print("\nTo start the bot, run:")
        print("   python chatbot.py")
    else:
        print("❌ Some tests failed. Please check your configuration.")
        print("\nCommon fixes:")
        print("1. Make sure .env file exists and has correct values")
        print("2. Check DeepSeek API key at: https://platform.deepseek.com/api_keys")
        print("3. Verify Confluence credentials and permissions")
        print("4. For Confluence Cloud, use API token instead of password")
    
    print("\nFor more help, see LLM_INTEGRATION_SUMMARY.md")

if __name__ == "__main__":
    main()