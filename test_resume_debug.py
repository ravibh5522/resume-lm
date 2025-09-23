#!/usr/bin/env python3
"""
Test script to check what resume content looks like
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents import OpenAIClient, ResumeGeneratorAgent
from models import StructuredResumeData, UserProfile, Experience, Education, ResumeGeneratorResponse

load_dotenv()

def test_resume_output():
    """Test what the resume generator actually outputs"""
    print("🧪 Testing resume generator output...")
    
    try:
        client = OpenAIClient()
        agent = ResumeGeneratorAgent(client)
        
        # Create ResumeData (not StructuredResumeData)
        from models import ResumeData, Project
        
        resume_data = ResumeData(
            profile=UserProfile(
                name='John Doe',
                location='San Francisco',
                email='john@example.com',
                phone='555-123-4567',
                linkedin='linkedin.com/in/johndoe',
                github='github.com/johndoe'
            ),
            experiences=[Experience(
                company='Tech Co',
                position='Software Engineer',
                start_date='2020-01-01',
                end_date='2024-01-01',
                description=['Built web applications with React and Node.js', 'Led team of 3 developers', 'Improved performance by 40%'],
                location='San Francisco'
            )],
            education=[Education(
                institution='UC Berkeley',
                degree='Bachelor of Science',
                field='Computer Science',
                start_date='2016-01-01',
                end_date='2020-01-01',
                location='Berkeley'
            )],
            skills=['Python', 'JavaScript', 'React', 'Node.js', 'AWS'],
            projects=[Project(
                name='E-commerce Platform',
                description='Built a full-stack e-commerce platform',
                technologies=['React', 'Node.js', 'PostgreSQL'],
                url='https://github.com/johndoe/ecommerce'
            )]
        )
        
        # Test the messages creation
        user_data_prompt = agent._create_enhanced_prompt(resume_data)
        messages = [
            {"role": "system", "content": agent.system_prompt},
            {"role": "user", "content": user_data_prompt}
        ]
        
        print("✅ Messages created successfully!")
        print(f"📄 System prompt length: {len(agent.system_prompt)} characters")
        print(f"📄 User prompt length: {len(user_data_prompt)} characters")
        
        # Get the raw response to see what's happening
        response = client.get_parsed_completion(messages, ResumeGeneratorResponse)
        
        if response and hasattr(response, 'markdown_resume'):
            print("✅ Resume generator working!")
            print("\n=== RAW RESUME OUTPUT (first 500 chars) ===")
            print(repr(response.markdown_resume[:500]))
            print("\n=== FORMATTED RESUME OUTPUT (first 1000 chars) ===")
            print(response.markdown_resume[:1000])
            print(f"\n📄 Total length: {len(response.markdown_resume)} characters")
            
            # Save to file for inspection
            with open('debug_resume.md', 'w') as f:
                f.write(response.markdown_resume)
            print("📁 Full resume saved to debug_resume.md")
            
            return True
        else:
            print("❌ Resume generator not working - no content returned")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing resume generator: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_resume_output()