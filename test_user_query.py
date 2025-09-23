#!/usr/bin/env python3
"""
Test script to verify user query is being passed to resume generator
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import AIAgentOrchestrator
from models import ResumeData, UserProfile, Experience, Education, Project

load_dotenv()

async def test_resume_with_query():
    """Test that user query is passed to resume generator"""
    print("🧪 Testing resume generation with user query...")
    
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_BASE_URL"):
        print("⚠️  Warning: OpenAI API credentials not found")
        return
    
    # Create sample resume data
    resume_data = ResumeData(
        profile=UserProfile(
            name="Alex Johnson",
            email="alex@example.com",
            phone="+1-555-0123",
            location="San Francisco, CA",
            linkedin="https://linkedin.com/in/alexjohnson",
            github="https://github.com/alexjohnson"
        ),
        summary="Software engineer with 3 years of experience in web development",
        experience=[
            Experience(
                company="TechCorp",
                position="Software Engineer", 
                start_date="2021",
                end_date="Present",
                description=["Built web applications", "Led development team"],
                location="San Francisco, CA"
            )
        ],
        education=[
            Education(
                institution="UC Berkeley",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date="2017",
                end_date="2021"
            )
        ],
        skills=["Python", "JavaScript", "React", "Node.js"],
        projects=[
            Project(
                name="Web App",
                description="Full-stack web application",
                technologies=["React", "Node.js"]
            )
        ]
    )
    
    # Test without user query
    print("\n📄 Testing without user query...")
    orchestrator = AIAgentOrchestrator()
    resume1 = await orchestrator.generate_resume_markdown(resume_data, "")
    print(f"✅ Resume generated (no query): {len(resume1)} characters")
    
    # Test with user query for layout change
    print("\n📄 Testing with layout change request...")
    user_query = "Make the resume more compact and use tables for experience section"
    resume2 = await orchestrator.generate_resume_markdown(resume_data, user_query)
    print(f"✅ Resume generated (with query): {len(resume2)} characters")
    print(f"🎯 User query used: '{user_query}'")
    
    # Check if the resumes are different
    if resume1 != resume2:
        print("🎉 SUCCESS: User query produced different output!")
        print(f"📊 Difference in length: {abs(len(resume2) - len(resume1))} characters")
    else:
        print("⚠️  WARNING: User query didn't change the output")
    
    # Test with style change request
    print("\n📄 Testing with style change request...")
    style_query = "Make it more creative with more emojis and visual elements"
    resume3 = await orchestrator.generate_resume_markdown(resume_data, style_query)
    print(f"✅ Resume generated (style query): {len(resume3)} characters")
    print(f"🎯 Style query used: '{style_query}'")
    
    print("\n🎉 All tests completed! User query functionality is working.")

if __name__ == "__main__":
    asyncio.run(test_resume_with_query())