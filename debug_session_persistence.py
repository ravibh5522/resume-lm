#!/usr/bin/env python3
"""
Debug script to test session management and data persistence
"""

import asyncio
import json
from datetime import datetime
from models import ResumeData, UserProfile, Experience, Education, Project, ChatMessage, ChatRole
from session_manager import SessionManager
from agents import AIAgentOrchestrator

async def test_session_persistence():
    """Test if session data persists correctly through modifications"""
    
    print("🔍 Testing Session Management & Data Persistence")
    print("=" * 60)
    
    # Initialize components
    session_manager = SessionManager()
    orchestrator = AIAgentOrchestrator()
    
    # Create a session with comprehensive resume data
    session_id = session_manager.create_session()
    print(f"📝 Created session: {session_id}")
    
    # Create comprehensive resume data
    complete_resume = ResumeData(
        profile=UserProfile(
            name="John Doe",
            email="john.doe@email.com",
            phone="+1-555-0123",
            location="San Francisco, CA",
            linkedin="https://linkedin.com/in/johndoe",
            github="https://github.com/johndoe"
        ),
        summary="Experienced Software Engineer with 5+ years in full-stack development.",
        experience=[
            Experience(
                company="Tech Corp",
                position="Senior Software Engineer", 
                start_date="2020",
                end_date="Present",
                description=["Led team of 5 engineers", "Increased performance by 40%"],
                location="San Francisco, CA"
            ),
            Experience(
                company="StartupXYZ",
                position="Software Developer",
                start_date="2018", 
                end_date="2020",
                description=["Built scalable APIs", "Worked with React and Node.js"],
                location="Palo Alto, CA"
            )
        ],
        education=[
            Education(
                institution="Stanford University",
                degree="Master of Science",
                field="Computer Science",
                start_date="2016",
                end_date="2018",
                gpa="3.8"
            ),
            Education(
                institution="UC Berkeley",
                degree="Bachelor of Science", 
                field="Computer Engineering",
                start_date="2012",
                end_date="2016",
                gpa="3.6"
            )
        ],
        skills=["Python", "JavaScript", "React", "Node.js", "AWS", "Docker", "Kubernetes"],
        projects=[
            Project(
                name="AI Resume Builder",
                description="Built an AI-powered resume generation platform",
                technologies=["Python", "FastAPI", "OpenAI", "React"]
            ),
            Project(
                name="E-commerce Platform", 
                description="Full-stack e-commerce solution with microservices",
                technologies=["Node.js", "React", "PostgreSQL", "Docker"]
            )
        ],
        certifications=["AWS Solutions Architect", "Certified Kubernetes Administrator"],
        languages=["English (Native)", "Spanish (Professional)"]
    )
    
    # Store initial data
    print("\n1️⃣ Storing initial comprehensive resume data...")
    session_manager.update_resume_data(session_id, complete_resume)
    
    # Verify initial storage
    session = session_manager.get_session(session_id)
    if session and session.user_data:
        print(f"✅ Initial data stored successfully:")
        print(f"   👤 Name: {session.user_data.profile.name}")
        print(f"   💼 Experience entries: {len(session.user_data.experience)}")
        print(f"   🎓 Education entries: {len(session.user_data.education)}") 
        print(f"   🚀 Projects: {len(session.user_data.projects)}")
        print(f"   ⚡ Skills: {len(session.user_data.skills)}")
    else:
        print("❌ Failed to store initial data")
        return
    
    # Simulate chat history
    chat_history = [
        ChatMessage(role=ChatRole.USER, content="Generate my resume"),
        ChatMessage(role=ChatRole.ASSISTANT, content="I'll create your resume now"),
        ChatMessage(role=ChatRole.USER, content="Change my name to Jane Smith")
    ]
    
    # Add chat messages to session
    for msg in chat_history:
        session_manager.add_chat_message(session_id, msg)
    
    print(f"\n2️⃣ Added {len(chat_history)} chat messages to history")
    
    # Test modification request - change name only
    print("\n3️⃣ Testing modification: Change name only...")
    
    # Get current session data before processing
    session_before = session_manager.get_session(session_id)
    print(f"📊 Before modification:")
    if session_before and session_before.user_data:
        print(f"   👤 Name: {session_before.user_data.profile.name}")
        print(f"   💼 Experience: {len(session_before.user_data.experience)} entries")
        print(f"   🎓 Education: {len(session_before.user_data.education)} entries")
        print(f"   🚀 Projects: {len(session_before.user_data.projects)} entries")
        print(f"   ⚡ Skills: {len(session_before.user_data.skills)} items")
    
    # Process the modification request
    response_text, updated_resume_data = await orchestrator.process_chat_message(
        "Change my name to Jane Smith",
        session_before.chat_history if session_before else [],
        session_before.user_data if session_before else None  # Pass existing resume data
    )
    
    print(f"\n🤖 AI Response: {response_text}")
    
    # Check if resume data was updated
    if updated_resume_data:
        print("\n⚠️  AI triggered full resume regeneration!")
        print("📊 Updated resume data:")
        print(f"   👤 Name: {updated_resume_data.profile.name}")
        print(f"   💼 Experience: {len(updated_resume_data.experience)} entries")
        print(f"   🎓 Education: {len(updated_resume_data.education)} entries")
        print(f"   🚀 Projects: {len(updated_resume_data.projects)} entries")
        print(f"   ⚡ Skills: {len(updated_resume_data.skills)} items")
        
        # Update session with new data
        session_manager.update_resume_data(session_id, updated_resume_data)
        
        # Check what was preserved vs reset
        print("\n🔍 Data Comparison:")
        original_exp = session_before.user_data.experience if session_before else []
        updated_exp = updated_resume_data.experience
        
        if len(original_exp) != len(updated_exp):
            print(f"❌ Experience count changed: {len(original_exp)} → {len(updated_exp)}")
        else:
            print(f"✅ Experience count preserved: {len(updated_exp)} entries")
            
        original_edu = session_before.user_data.education if session_before else []
        updated_edu = updated_resume_data.education
        
        if len(original_edu) != len(updated_edu):
            print(f"❌ Education count changed: {len(original_edu)} → {len(updated_edu)}")
        else:
            print(f"✅ Education count preserved: {len(updated_edu)} entries")
            
        if updated_resume_data.profile.name == "Jane Smith":
            print("✅ Name updated correctly")
        else:
            print(f"❌ Name not updated correctly: {updated_resume_data.profile.name}")
            
    else:
        print("\n✅ AI did not trigger full regeneration (good for small changes)")
    
    # Final session state check
    print("\n4️⃣ Final session state:")
    final_session = session_manager.get_session(session_id)
    if final_session and final_session.user_data:
        print(f"   👤 Final Name: {final_session.user_data.profile.name}")
        print(f"   💼 Final Experience: {len(final_session.user_data.experience)} entries")
        print(f"   🎓 Final Education: {len(final_session.user_data.education)} entries")
        print(f"   🚀 Final Projects: {len(final_session.user_data.projects)} entries")
        print(f"   ⚡ Final Skills: {len(final_session.user_data.skills)} items")
        print(f"   💬 Chat History: {len(final_session.chat_history)} messages")
        
        # Check for data loss
        if len(final_session.user_data.experience) < 2:
            print("❌ CRITICAL: Experience data was lost!")
        if len(final_session.user_data.education) < 2:
            print("❌ CRITICAL: Education data was lost!")
        if len(final_session.user_data.projects) < 2:
            print("❌ CRITICAL: Project data was lost!")
        if len(final_session.user_data.skills) < 5:
            print("❌ CRITICAL: Skills data was lost!")
    
    print("\n🔚 Session persistence test completed")

if __name__ == "__main__":
    asyncio.run(test_session_persistence())