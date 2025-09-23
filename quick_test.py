#!/usr/bin/env python3
"""
Quick test of the enhanced resume generation system
"""

import asyncio
import sys
import os
sys.path.insert(0, '/home/ravi/Desktop/resume-lm')

from agents import AIAgentOrchestrator
from models import ResumeData, UserProfile, Experience, Education

async def test_simple_generation():
    """Test basic resume generation"""
    print("🧪 Testing Resume Generation...")
    
    # Create test data
    test_data = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john.doe@email.com", 
            phone="+1-555-0123",
            location="San Francisco, CA"
        ),
        summary="Experienced software engineer with passion for AI",
        skills=["Python", "JavaScript", "React", "Node.js"],
        experience=[Experience(
            company="TechCorp",
            position="Software Engineer",
            start_date="2020",
            end_date="Present",
            description=["Built scalable applications", "Led team of 5 developers"]
        )],
        education=[Education(
            institution="UC Berkeley",
            degree="BS",
            field="Computer Science", 
            start_date="2016",
            end_date="2020"
        )]
    )
    
    # Generate resume
    orchestrator = AIAgentOrchestrator()
    try:
        markdown = await orchestrator.generate_resume_markdown(test_data)
        print("✅ Resume generated successfully!")
        print(f"📄 Length: {len(markdown)} characters")
        print("📋 First 300 characters:")
        print("-" * 50)
        print(markdown[:300] + "...")
        print("-" * 50)
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_simple_generation())
    if result:
        print("🎉 System is working!")
    else:
        print("⚠️  System needs attention")