#!/usr/bin/env python3
"""
Test script for the enhanced AI Resume Generator
Tests the structured output and modern resume generation features
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import AIAgentOrchestrator
from models import ChatMessage, ChatRole, ResumeData, UserProfile, Experience, Education, Project

load_dotenv()

async def test_data_gathering():
    """Test the enhanced data gathering agent with structured outputs"""
    print("🧪 Testing Enhanced Data Gathering Agent...")
    
    orchestrator = AIAgentOrchestrator()
    
    # Simulate a conversation
    chat_history = []
    
    # Test message
    test_message = """Hi! I'm John Doe, a software engineer. I work at TechCorp as a Senior Software Engineer. 
    I have experience with Python, JavaScript, React, and Node.js. I have a CS degree from UC Berkeley. 
    My email is john.doe@email.com and I'm located in San Francisco, CA."""
    
    try:
        response, resume_data = await orchestrator.process_chat_message(test_message, chat_history)
        
        print(f"✅ Response: {response}")
        
        if resume_data:
            print("✅ Resume data extracted successfully!")
            print(f"📊 Profile: {resume_data.profile.name}")
            print(f"📧 Email: {resume_data.profile.email}")
            print(f"🎯 Skills: {resume_data.skills}")
        else:
            print("📝 More information needed, continuing conversation...")
            
    except Exception as e:
        print(f"❌ Error in data gathering test: {e}")

async def test_resume_generation():
    """Test the enhanced resume generation with modern styling"""
    print("\n🎨 Testing Enhanced Resume Generator...")
    
    orchestrator = AIAgentOrchestrator()
    
    # Create test resume data
    test_data = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john.doe@email.com",
            phone="+1-555-0123",
            location="San Francisco, CA",
            linkedin="linkedin.com/in/johndoe",
            github="github.com/johndoe"
        ),
        summary="Experienced software engineer specializing in AI and web development",
        experience=[
            Experience(
                company="TechCorp Inc.",
                position="Senior Software Engineer",
                start_date="January 2021",
                end_date="Present",
                description=[
                    "Led development of AI-powered features serving 10M+ users",
                    "Improved system performance by 40% through optimization",
                    "Mentored team of 5 junior developers"
                ],
                location="San Francisco, CA"
            )
        ],
        education=[
            Education(
                institution="UC Berkeley",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date="2015",
                end_date="2019",
                gpa="3.8"
            )
        ],
        skills=["Python", "JavaScript", "React", "Node.js", "AWS", "Docker"],
        projects=[
            Project(
                name="AI Resume Builder",
                description="Revolutionary AI-powered resume generation platform",
                technologies=["React", "FastAPI", "OpenAI", "Docker"],
                url="https://resume-ai.tech",
                github="https://github.com/johndoe/ai-resume"
            )
        ],
        certifications=["AWS Certified Solutions Architect"],
        languages=["English (Native)", "Spanish (Professional)"]
    )
    
    try:
        markdown = await orchestrator.generate_resume_markdown(test_data)
        
        print("✅ Modern resume generated successfully!")
        print("📄 Preview (first 500 characters):")
        print("-" * 50)
        print(markdown[:500] + "..." if len(markdown) > 500 else markdown)
        print("-" * 50)
        
        # Check for modern elements
        modern_indicators = [
            "🚀" in markdown or "💡" in markdown,  # Emojis
            "**" in markdown,  # Bold formatting
            "`" in markdown,   # Code formatting
            "---" in markdown, # Horizontal rules
        ]
        
        if any(modern_indicators):
            print("✅ Modern formatting elements detected!")
        else:
            print("⚠️  Modern formatting may need adjustment")
            
    except Exception as e:
        print(f"❌ Error in resume generation test: {e}")

async def test_performance():
    """Test performance improvements"""
    print("\n⚡ Testing Performance Improvements...")
    
    import time
    
    orchestrator = AIAgentOrchestrator()
    
    # Create a realistic test case
    test_data = ResumeData(
        profile=UserProfile(name="Test User", email="test@example.com"),
        summary="Test professional with extensive experience",
        skills=["Python", "Machine Learning", "Data Science", "AWS"],
        experience=[Experience(
            company="Test Corp",
            position="Data Scientist",
            start_date="2020",
            description=["Analyzed large datasets", "Built ML models"]
        )]
    )
    
    try:
        start_time = time.time()
        markdown = await orchestrator.generate_resume_markdown(test_data)
        end_time = time.time()
        
        generation_time = end_time - start_time
        word_count = len(markdown.split())
        
        print(f"✅ Resume generated in {generation_time:.2f} seconds")
        print(f"📊 Generated {word_count} words")
        print(f"⚡ Performance: {word_count/generation_time:.1f} words/second")
        
        if generation_time < 10:  # Should be reasonably fast
            print("✅ Performance target met!")
        else:
            print("⚠️  Consider optimization for better performance")
            
    except Exception as e:
        print(f"❌ Error in performance test: {e}")

async def main():
    """Run all tests"""
    print("🚀 AI Resume Generator - Enhanced Testing Suite")
    print("=" * 60)
    
    # Check environment variables
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_BASE_URL"):
        print("⚠️  Warning: OpenAI API credentials not found in environment")
        print("   Set OPENAI_API_KEY and OPENAI_BASE_URL to run live tests")
        return
    
    await test_data_gathering()
    await test_resume_generation()
    await test_performance()
    
    print("\n🎉 Testing completed!")
    print("📝 See PERFORMANCE_IMPROVEMENTS.md for detailed enhancement documentation")

if __name__ == "__main__":
    asyncio.run(main())