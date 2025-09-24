#!/usr/bin/env python3
"""
Debug script to test what the AI actually sees and returns
"""

import asyncio
from models import ResumeData, UserProfile, Experience, Education, Project, ChatMessage, ChatRole
from agents import DataGatheringAgent, OpenAIClient

async def debug_ai_context():
    """Debug what the AI actually sees and returns"""
    
    print("🔍 Debugging AI Context and Response")
    print("=" * 50)
    
    # Create test data
    existing_data = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john.doe@email.com",
            phone="+1-555-0123",
            location="San Francisco, CA"
        ),
        summary="Software Engineer with 5+ years experience",
        experience=[
            Experience(
                company="Tech Corp",
                position="Senior Engineer",
                start_date="2020",
                end_date="Present",
                description=["Led team", "Built systems"]
            )
        ],
        skills=["Python", "JavaScript", "React"]
    )
    
    # Create agent
    client = OpenAIClient()
    agent = DataGatheringAgent(client)
    
    # Test message
    chat_history = [
        ChatMessage(role=ChatRole.USER, content="Generate my resume"),
        ChatMessage(role=ChatRole.ASSISTANT, content="I'll create your resume")
    ]
    
    print("📤 Sending to AI:")
    print(f"   Message: 'Change my name to Jane Smith'")
    print(f"   Existing Data: Name={existing_data.profile.name}, Skills={len(existing_data.skills)}, Experience={len(existing_data.experience)}")
    print(f"   Chat History: {len(chat_history)} messages")
    
    try:
        response, resume_data = await agent.process_message(
            "Change my name to Jane Smith", 
            chat_history, 
            existing_data
        )
        
        print(f"\n📥 AI Response:")
        print(f"   Message: {response}")
        print(f"   Resume Data Returned: {resume_data is not None}")
        
        if resume_data:
            print(f"   Updated Name: {resume_data.profile.name}")
            print(f"   Skills Count: {len(resume_data.skills)}")
            print(f"   Experience Count: {len(resume_data.experience)}")
            print(f"   Summary: {resume_data.summary}")
        else:
            print("   No resume data returned - AI did not trigger generation")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_ai_context())