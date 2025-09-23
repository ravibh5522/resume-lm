#!/usr/bin/env python3
"""
Test script for the enhanced resume generator with structured outputs
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import OpenAIClient, ResumeGeneratorAgent
from models import ResumeData, UserProfile, Experience, Education, Project

load_dotenv()

def create_sample_resume_data():
    """Create sample resume data for testing"""
    return ResumeData(
        profile=UserProfile(
            name="John Smith",
            email="john.smith@email.com",
            phone="(555) 123-4567",
            location="San Francisco, CA",
            linkedin="https://linkedin.com/in/johnsmith",
            github="https://github.com/johnsmith"
        ),
        summary="Experienced software engineer with 5+ years in full-stack development",
        experience=[
            Experience(
                company="Tech Corp",
                position="Senior Software Engineer",
                start_date="2021",
                end_date="Present",
                description=[
                    "Led development of microservices architecture serving 1M+ users",
                    "Reduced deployment time by 60% through CI/CD improvements",
                    "Mentored 3 junior developers"
                ],
                location="San Francisco, CA"
            )
        ],
        education=[
            Education(
                institution="University of California",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date="2015",
                end_date="2019",
                gpa="3.8"
            )
        ],
        skills=[
            "Python", "JavaScript", "React", "Node.js", "AWS", "Docker"
        ],
        projects=[
            Project(
                name="Task Manager App",
                description="Full-stack web application for team task management",
                technologies=["React", "Node.js", "PostgreSQL"],
                github="https://github.com/johnsmith/taskmanager"
            )
        ],
        certifications=["AWS Certified Solutions Architect"],
        languages=["English (Native)", "Spanish (Conversational)"]
    )

async def test_structured_resume_generation():
    """Test the resume generator with structured outputs"""
    print("🚀 Testing Enhanced Resume Generator with Structured Outputs")
    print("=" * 60)
    
    if not os.getenv("OPENAI_API_KEY") or not os.getenv("OPENAI_BASE_URL"):
        print("⚠️  Warning: OpenAI API credentials not found")
        return False
    
    try:
        # Initialize OpenAI client and resume generator
        openai_client = OpenAIClient()
        resume_generator = ResumeGeneratorAgent(openai_client)
        
        # Create sample data
        print("📋 Creating sample resume data...")
        resume_data = create_sample_resume_data()
        
        # Generate resume using structured outputs
        print("🎨 Generating resume with structured outputs...")
        resume_markdown = await resume_generator.generate_resume(resume_data)
        
        if resume_markdown:
            print("✅ Resume generation successful!")
            print(f"📄 Resume length: {len(resume_markdown)} characters")
            
            # Show a preview of the generated resume
            print("\n📝 Resume Preview (first 500 characters):")
            print("-" * 50)
            print(resume_markdown[:500] + "..." if len(resume_markdown) > 500 else resume_markdown)
            print("-" * 50)
            
            # Save to file for inspection
            with open('test_generated_resume.md', 'w') as f:
                f.write(resume_markdown)
            print("💾 Full resume saved to: test_generated_resume.md")
            
            return True
        else:
            print("❌ Resume generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Error testing resume generation: {e}")
        return False

async def main():
    """Run the test"""
    success = await test_structured_resume_generation()
    
    if success:
        print("\n🎉 Resume generator with structured outputs is working!")
    else:
        print("\n⚠️  Resume generator needs attention")
    
    print("\n📝 Note: The generator now uses structured outputs for better consistency")

if __name__ == "__main__":
    asyncio.run(main())