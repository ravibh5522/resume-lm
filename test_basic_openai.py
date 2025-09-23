#!/usr/bin/env python3
"""
Simple test for OpenAI client functionality
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import OpenAIClient

load_dotenv()

def test_basic_completion():
    """Test basic OpenAI completion"""
    print("🧪 Testing basic OpenAI completion...")
    
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_BASE_URL"):
        print("⚠️  Warning: OpenAI API credentials not found")
        return False
    
    try:
        client = OpenAIClient()
        print(f"📦 Using model: {client.model}")
        
        # Test basic completion
        response = client.client.chat.completions.create(
            model=client.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in a structured way."}
            ],
            temperature=0.7
        )
        
        if response and response.choices:
            print("✅ Basic completion working!")
            print(f"📄 Response: {response.choices[0].message.content}")
            return True
        else:
            print("❌ Basic completion failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing basic completion: {e}")
        return False

def test_json_mode():
    """Test JSON mode completion"""
    print("\n🧪 Testing JSON mode completion...")
    
    try:
        client = OpenAIClient()
        
        # Test JSON mode
        response = client.client.chat.completions.create(
            model=client.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Always respond with valid JSON."},
                {"role": "user", "content": "Return a simple greeting in JSON format with 'message' and 'status' fields."}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        if response and response.choices:
            content = response.choices[0].message.content
            print("✅ JSON mode working!")
            print(f"📄 JSON Response: {content}")
            
            # Try to parse JSON
            import json
            parsed = json.loads(content or "{}")
            print(f"🔧 Parsed JSON: {parsed}")
            return True
        else:
            print("❌ JSON mode failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing JSON mode: {e}")
        return False

def main():
    """Run tests"""
    print("🚀 Testing OpenAI Client Functionality")
    print("=" * 50)
    
    test1 = test_basic_completion()
    test2 = test_json_mode()
    
    if test1 and test2:
        print("\n🎉 All tests passed! OpenAI client is working.")
    elif test1 or test2:
        print("\n⚠️  Some tests passed, some issues remain.")
    else:
        print("\n❌ All tests failed. Check your OpenAI configuration.")

if __name__ == "__main__":
    main()