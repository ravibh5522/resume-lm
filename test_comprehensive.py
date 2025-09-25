#!/usr/bin/env python3
"""
Comprehensive test for the enhanced AI Resume Generator with DOC/DOCX support
Tests all major components and new features
"""

import sys
import os
import asyncio
import json
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

def test_imports():
    """Test all critical imports"""
    print("🔍 Testing imports...")
    
    try:
        # Core components
        from models import (
            ChatRequest, ChatResponse, DocxGenerationRequest, DocxResponse,
            ResumeData, UserProfile, Experience, Education
        )
        print("  ✅ Models imported successfully")
        
        from session_manager import SessionManager
        print("  ✅ Session manager imported successfully")
        
        from agents import AIAgentOrchestrator
        print("  ✅ AI agents imported successfully")
        
        from pdf_generator_optimized import OptimizedPDFGenerator
        print("  ✅ PDF generator imported successfully")
        
        from docx_generator import ProfessionalDocxGenerator
        print("  ✅ DOCX generator imported successfully")
        
        from resume_modifier import ResumeModifier
        print("  ✅ Resume modifier imported successfully")
        
        # FastAPI components
        import fastapi
        import uvicorn
        import websockets
        import redis
        print("  ✅ FastAPI and dependencies imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Import error: {e}")
        return False

def test_docx_generation():
    """Test DOCX generation functionality"""
    print("\n📝 Testing DOCX generation...")
    
    try:
        from docx_generator import ProfessionalDocxGenerator
        
        sample_markdown = """# John Doe
john.doe@example.com | (555) 123-4567 | New York, NY

## Professional Summary
Software engineer with 5 years of experience.

## Experience
**Senior Developer**
*Tech Company | 2020 - Present*
- Led development of web applications
- Improved performance by 40%

## Education
**Bachelor of Computer Science**
*University of Technology | 2015 - 2019*

## Skills
Python, JavaScript, React, Django, AWS, Docker"""
        
        generator = ProfessionalDocxGenerator()
        
        # Test base64 generation
        docx_base64 = generator.generate_docx_base64(sample_markdown)
        
        if docx_base64:
            print(f"  ✅ DOCX base64 generation: Success ({len(docx_base64)} chars)")
            
            # Test file saving
            success = generator.save_docx_file(sample_markdown, "test_comprehensive.docx")
            if success:
                print("  ✅ DOCX file generation: Success")
                return True
            else:
                print("  ❌ DOCX file generation: Failed")
                return False
        else:
            print("  ❌ DOCX base64 generation: Failed")
            return False
            
    except Exception as e:
        print(f"  ❌ DOCX generation error: {e}")
        return False

def test_pdf_generation():
    """Test PDF generation functionality"""
    print("\n📄 Testing PDF generation...")
    
    try:
        from pdf_generator_optimized import OptimizedPDFGenerator
        
        sample_markdown = """# Jane Smith
jane.smith@example.com | (555) 987-6543 | San Francisco, CA

## Professional Summary
Product manager with 6 years of experience in tech startups.

## Experience
**Senior Product Manager**
*Innovation Corp | 2019 - Present*
- Launched 3 successful products
- Increased user engagement by 60%

## Education
**MBA in Business Administration**
*Stanford University | 2017 - 2019*

## Skills
Product Strategy, Analytics, Agile, Scrum, SQL, Python"""
        
        generator = OptimizedPDFGenerator()
        
        # Test base64 generation
        pdf_base64 = generator.generate_pdf_base64(sample_markdown)
        
        if pdf_base64:
            print(f"  ✅ PDF base64 generation: Success ({len(pdf_base64)} chars)")
            return True
        else:
            print("  ❌ PDF base64 generation: Failed")
            return False
            
    except Exception as e:
        print(f"  ❌ PDF generation error: {e}")
        return False

def test_session_management():
    """Test session management functionality"""
    print("\n🗄️ Testing session management...")
    
    try:
        from session_manager import SessionManager
        from models import ResumeData, UserProfile, ChatMessage, ChatRole
        
        # Test session creation
        manager = SessionManager()
        session_id = manager.create_session()
        
        if session_id:
            print(f"  ✅ Session creation: Success ({session_id})")
            
            # Test session retrieval
            session = manager.get_session(session_id)
            if session:
                print("  ✅ Session retrieval: Success")
                
                # Test data updates
                test_data = ResumeData(
                    profile=UserProfile(name="Test User", email="test@example.com")
                )
                success = manager.update_resume_data(session_id, test_data)
                if success:
                    print("  ✅ Resume data update: Success")
                    return True
                else:
                    print("  ❌ Resume data update: Failed")
                    return False
            else:
                print("  ❌ Session retrieval: Failed")
                return False
        else:
            print("  ❌ Session creation: Failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Session management error: {e}")
        return False

def test_models_validation():
    """Test Pydantic models and validation"""
    print("\n🏗️ Testing data models...")
    
    try:
        from models import (
            ChatRequest, DocxGenerationRequest, ResumeData, 
            UserProfile, Experience, Education
        )
        
        # Test basic models
        profile = UserProfile(
            name="Test User",
            email="test@example.com",
            phone="555-123-4567"
        )
        print("  ✅ UserProfile model: Valid")
        
        experience = Experience(
            company="Test Corp",
            position="Developer",
            start_date="2020",
            description=["Built amazing things"]
        )
        print("  ✅ Experience model: Valid")
        
        resume_data = ResumeData(
            profile=profile,
            experience=[experience],
            skills=["Python", "JavaScript"]
        )
        print("  ✅ ResumeData model: Valid")
        
        # Test request models
        chat_req = ChatRequest(
            message="Hello",
            session_id="test-session"
        )
        print("  ✅ ChatRequest model: Valid")
        
        docx_req = DocxGenerationRequest(
            markdown="# Test",
            session_id="test-session"
        )
        print("  ✅ DocxGenerationRequest model: Valid")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Model validation error: {e}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\n⚙️ Testing environment configuration...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        # Load environment variables
        load_dotenv()
        
        required_vars = [
            "OPENAI_API_KEY", "OPENAI_BASE_URL", "OPENAI_MODEL"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"  ⚠️ Missing environment variables: {', '.join(missing_vars)}")
            print("  💡 Update your .env file with actual values for full functionality")
        else:
            print("  ✅ All required environment variables present")
        
        # Check optional vars
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            print(f"  ✅ Redis configuration found: {redis_url}")
        else:
            print("  ℹ️ Redis not configured - will use in-memory storage")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Environment configuration error: {e}")
        return False

def run_comprehensive_test():
    """Run all tests"""
    print("🧪 AI Resume Generator - Comprehensive Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Config", test_environment_config), 
        ("Data Models", test_models_validation),
        ("Session Management", test_session_management),
        ("PDF Generation", test_pdf_generation),
        ("DOCX Generation", test_docx_generation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"  ❌ {test_name}: Exception - {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<25} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Your AI Resume Generator is ready!")
        print("\n🚀 To start the application:")
        print("   1. Update .env with your OpenAI API credentials")
        print("   2. Run: source venv/bin/activate")
        print("   3. Run: python main.py")
        print("   4. Open: http://localhost:8000")
        print("\n✨ Features ready:")
        print("   • Real-time AI chat for resume creation")
        print("   • Dual-format preview (PDF + DOCX)")
        print("   • Live editing and modifications") 
        print("   • Professional styling for both formats")
        print("   • ATS-optimized output")
        print("   • Instant downloads")
    else:
        print(f"\n⚠️ {failed} tests failed. Please fix the issues above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)