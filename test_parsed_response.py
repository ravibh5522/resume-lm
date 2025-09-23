#!/usr/bin/env python3
"""
Test script for the new response.parsed implementation
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import OpenAIClient
from models import DataGatheringResponse, StructuredResumeData, UserProfile

load_dotenv()

def test_response_parsed():
    """Test the new response.parsed functionality"""
    print("🧪 Testing response.parsed with Pydantic models...")
    
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_BASE_URL"):
        print("⚠️  Warning: OpenAI API credentials not found")
        return False
    
    try:
        client = OpenAIClient()
        
        # Test message
        messages = [
            {"role": "system", "content": "You are a helpful assistant that extracts information and responds in the specified format."},
            {"role": "user", "content": "Hi, I'm John Doe, a software engineer from San Francisco. I want to create a resume."}
        ]
        
        # Test parsed response
        parsed_response = client.get_parsed_completion(
            messages, DataGatheringResponse
        )
        
        if parsed_response:
            print("✅ response.parsed working!")
            print(f"📄 Message: {parsed_response.message}")
            print(f"🔧 Needs more info: {parsed_response.needs_more_info}")
            if parsed_response.collected_data:
                print(f"👤 Profile name: {parsed_response.collected_data.profile.name}")
            return True
        else:
            print("❌ response.parsed not working")
            return False
            
    except Exception as e:
        print(f"❌ Error testing response.parsed: {e}")
        return False

async def test_fallback_json():
    """Test the fallback JSON mode"""
    print("\n🧪 Testing fallback JSON mode...")
    
    try:
        client = OpenAIClient()
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, generate a simple response."}
        ]
        
        schema_description = """Return a JSON object with:
{
  "message": "your response text",
  "status": "success"
}"""
        
        result = await client.get_structured_completion(messages, schema_description)
        
        if result and isinstance(result, dict):
            print("✅ Fallback JSON mode working!")
            print(f"📄 Result: {result}")
            return True
        else:
            print("❌ Fallback JSON mode failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing fallback: {e}")
        return False

async def main():
    """Run tests"""
    print("🚀 Testing Enhanced Structured Outputs")
    print("=" * 50)
    
    test1 = test_response_parsed()  # This one is synchronous
    test2 = await test_fallback_json()  # This one is async
    
    if test1 or test2:
        print("\n🎉 At least one method is working!")
    else:
        print("\n⚠️  Both methods need attention")
    
    print("\n📝 Note: If response.parsed fails, the system will use fallback JSON mode")

if __name__ == "__main__":
    asyncio.run(main())