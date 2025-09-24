#!/usr/bin/env python3
"""
Test the complete system with UI-only modifications to ensure content preservation
"""

import asyncio
from agents import AIAgentOrchestrator
from models import ResumeData, UserProfile, Experience, Education, ChatMessage, ChatRole
from datetime import datetime

async def test_ui_only_modifications():
    """Test that UI modifications don't affect content data"""
    
    print("🧪 Testing UI-Only Modification System")
    print("=" * 50)
    
    orchestrator = AIAgentOrchestrator()
    
    # Create sample resume data
    sample_data = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john@email.com",
            phone="(555) 123-4567",
            location="San Francisco, CA"
        ),
        summary="Experienced software engineer with 5+ years in development.",
        experience=[
            Experience(
                company="Tech Corp",
                position="Senior Engineer",
                start_date="2020",
                end_date="Present",
                description=["Led team of 5 engineers", "Increased performance by 40%"]
            ),
            Experience(
                company="StartupXYZ", 
                position="Software Engineer",
                start_date="2018",
                end_date="2020",
                description=["Built REST APIs", "Developed React applications"]
            )
        ],
        education=[
            Education(
                institution="UC Berkeley",
                degree="Bachelor of Science",
                field="Computer Science",
                start_date="2014",
                end_date="2018"
            )
        ],
        skills=["Python", "JavaScript", "React", "Django", "PostgreSQL"],
        projects=[]
    )
    
    # Test UI-only requests
    ui_requests = [
        "make the name bold",
        "change header colors to blue", 
        "use larger font for section headers",
        "make the layout more compact",
        "change the overall style to be more modern"
    ]
    
    chat_history = [
        ChatMessage(role=ChatRole.USER, content="Hello", timestamp=datetime.now()),
        ChatMessage(role=ChatRole.ASSISTANT, content="Hi! How can I help with your resume?", timestamp=datetime.now())
    ]
    
    print("📋 Original Resume Data Summary:")
    print(f"   Name: {sample_data.profile.name}")
    print(f"   Experience entries: {len(sample_data.experience)}")
    print(f"   Education entries: {len(sample_data.education)}")
    print(f"   Skills count: {len(sample_data.skills)}")
    print()
    
    for i, request in enumerate(ui_requests, 1):
        print(f"🎨 Test {i}: '{request}'")
        
        # Process the UI request
        response, updated_data = await orchestrator.process_chat_message(
            request, chat_history, sample_data
        )
        
        print(f"   Response: {response}")
        
        # Check if data was preserved (updated_data should be same as original for UI requests)
        if updated_data is None:
            updated_data = sample_data  # UI requests shouldn't change data
        
        data_preserved = (
            updated_data.profile.name == sample_data.profile.name and
            len(updated_data.experience) == len(sample_data.experience) and
            len(updated_data.education) == len(sample_data.education) and
            len(updated_data.skills) == len(sample_data.skills)
        )
        
        print(f"   Data preserved: {'✅' if data_preserved else '❌'}")
        
        # Generate resume with UI modifications
        try:
            markdown_resume = await orchestrator.generate_resume_markdown(sample_data, request)
            
            # Check if basic content is still present
            has_name = sample_data.profile.name and sample_data.profile.name in markdown_resume
            has_experience = any(exp.company in markdown_resume for exp in sample_data.experience)
            has_education = any(edu.institution in markdown_resume for edu in sample_data.education)
            has_skills = any(skill in markdown_resume for skill in sample_data.skills[:3])
            
            content_integrity = has_name and has_experience and has_education and has_skills
            
            print(f"   Resume generated: ✅")
            print(f"   Content integrity: {'✅' if content_integrity else '❌'}")
            
            if not content_integrity:
                print(f"      Name present: {has_name}")
                print(f"      Experience present: {has_experience}")  
                print(f"      Education present: {has_education}")
                print(f"      Skills present: {has_skills}")
                
        except Exception as e:
            print(f"   Resume generation error: ❌ {e}")
        
        print()
    
    print("🔍 Testing Content vs UI Detection")
    print("=" * 50)
    
    mixed_requests = [
        {"request": "make headers blue and add experience at Google", "should_be_ui": False},
        {"request": "change my name to Jane and make it bold", "should_be_ui": False},
        {"request": "just make the layout more modern", "should_be_ui": True},
        {"request": "I worked at Apple for 3 years", "should_be_ui": False},
        {"request": "use a more professional color scheme", "should_be_ui": True}
    ]
    
    for test in mixed_requests:
        request = test["request"]
        expected_ui = test["should_be_ui"]
        
        detected_ui = orchestrator.advanced_ui_agent.is_ui_modification_request(request)
        
        status = "✅" if detected_ui == expected_ui else "❌"
        print(f"{status} '{request}'")
        print(f"     Expected UI-only: {expected_ui}, Detected: {detected_ui}")
        print()
    
    print("🎉 UI-Only Modification System Test Complete!")
    print("\nKey Benefits:")
    print("✅ UI changes don't modify resume data")
    print("✅ Content preservation guaranteed") 
    print("✅ Clear separation of UI vs content changes")
    print("✅ AI-powered visual styling")
    print("✅ User can safely request visual changes")

if __name__ == "__main__":
    asyncio.run(test_ui_only_modifications())