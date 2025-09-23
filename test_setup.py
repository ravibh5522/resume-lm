#!/usr/bin/env python3
"""
Test script for AI Resume Generator
Tests the core functionality without requiring the full server setup
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import ChatMessage, ChatRole, ResumeData, UserProfile
from agents import AIAgentOrchestrator
from session_manager import SessionManager

async def test_ai_agents():
    """Test the AI agents functionality"""
    print("🧪 Testing AI Resume Generator Components...")
    
    # Load environment variables
    load_dotenv()
    
    # Check if required environment variables are set
    required_vars = ["OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {', '.join(missing_vars)}")
        print("Please check your .env file")
        return False
    
    print("✅ Environment variables loaded")
    
    # Test session manager
    print("\n📝 Testing Session Manager...")
    session_manager = SessionManager()
    
    # Create a test session
    session_id = session_manager.create_session()
    print(f"✅ Created session: {session_id}")
    
    # Test session retrieval
    session = session_manager.get_session(session_id)
    if session:
        print("✅ Session retrieved successfully")
    else:
        print("❌ Failed to retrieve session")
        return False
    
    # Test AI orchestrator
    print("\n🤖 Testing AI Orchestrator...")
    ai_orchestrator = AIAgentOrchestrator()
    
    # Create some test chat history
    chat_history = [
        ChatMessage(role=ChatRole.USER, content="Hi, I need help creating a resume"),
        ChatMessage(role=ChatRole.ASSISTANT, content="I'd be happy to help you create a professional resume! Let's start with some basic information. What's your name?"),
        ChatMessage(role=ChatRole.USER, content="My name is John Doe")
    ]
    
    # Test chat processing
    try:
        response, resume_data = await ai_orchestrator.process_chat_message(
            "I'm a software engineer with 5 years of experience at Google working on machine learning projects.",
            chat_history
        )
        print(f"✅ AI response received: {response[:100]}...")
        
        if resume_data:
            print("✅ Resume data extracted successfully")
            # Test resume generation
            print("\n📄 Testing Resume Generation...")
            resume_markdown = await ai_orchestrator.generate_resume_markdown(resume_data)
            print(f"✅ Resume generated ({len(resume_markdown)} characters)")
            print(f"Preview: {resume_markdown[:200]}...")
        else:
            print("ℹ️  No resume data extracted (expected for this test)")
            
    except Exception as e:
        print(f"❌ AI processing failed: {e}")
        return False
    
    # Test resume generation with sample data
    print("\n📄 Testing Resume Generation with Sample Data...")
    sample_resume_data = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john.doe@email.com",
            phone="+1-555-0123",
            location="San Francisco, CA",
            linkedin="linkedin.com/in/johndoe",
            github="github.com/johndoe"
        ),
        summary="Experienced software engineer specializing in machine learning and web development",
        experience=[],
        skills=["Python", "JavaScript", "Machine Learning", "React", "Node.js"]
    )
    
    try:
        resume_markdown = await ai_orchestrator.generate_resume_markdown(sample_resume_data)
        print(f"✅ Sample resume generated ({len(resume_markdown)} characters)")
        
        # Save sample resume for inspection
        with open("sample_resume.md", "w") as f:
            f.write(resume_markdown)
        print("✅ Sample resume saved to sample_resume.md")
        
    except Exception as e:
        print(f"❌ Resume generation failed: {e}")
        return False
    
    print("\n🎉 All tests passed successfully!")
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python main.py")
    print("3. Or use Docker: ./deploy.sh")
    print("4. Access the application at http://localhost:8000")
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_ai_agents())
    sys.exit(0 if success else 1)