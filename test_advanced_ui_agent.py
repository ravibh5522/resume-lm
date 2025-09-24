#!/usr/bin/env python3
"""
Test the Advanced UI Agent to ensure it only modifies UI/styling and preserves content
"""

import asyncio
from advanced_ui_agent import AdvancedUIAgent

async def test_ui_agent():
    """Test the advanced UI agent with various scenarios"""
    
    agent = AdvancedUIAgent()
    
    # Sample resume content
    sample_resume = """# John Doe

San Francisco, CA | john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

## Professional Summary

Experienced software engineer with 5+ years of experience in full-stack development.

## Experience

**Senior Software Engineer** | Tech Corp | 2020 - Present
- Led development team of 5 engineers
- Increased system performance by 40%
- Implemented microservices architecture

**Software Engineer** | StartupXYZ | 2018 - 2020  
- Developed REST APIs using Python and Django
- Built responsive web applications with React
- Collaborated with product team on feature requirements

## Education

**Bachelor of Science in Computer Science** | UC Berkeley | 2014 - 2018
- GPA: 3.8/4.0
- Relevant Coursework: Data Structures, Algorithms, Software Engineering

## Skills

- **Programming Languages**: Python, JavaScript, Java, C++
- **Frameworks**: React, Django, Node.js, Express
- **Databases**: PostgreSQL, MongoDB, Redis
- **Tools**: Docker, Kubernetes, Git, Jenkins"""
    
    # Test cases: UI modifications vs content modifications
    test_cases = [
        # UI Modifications (should be detected)
        {"message": "make the name bold", "expected_ui": True},
        {"message": "change header colors to blue", "expected_ui": True},
        {"message": "use larger font for headers", "expected_ui": True},
        {"message": "make the layout more compact", "expected_ui": True},
        {"message": "change spacing between sections", "expected_ui": True},
        
        # Content Modifications (should NOT be detected as UI)
        {"message": "add my experience at Google", "expected_ui": False},
        {"message": "change my name to Jane Smith", "expected_ui": False},
        {"message": "I worked at Microsoft for 2 years", "expected_ui": False},
        {"message": "add Python and React to my skills", "expected_ui": False},
        {"message": "update my education to include MBA", "expected_ui": False},
        
        # Mixed requests (content should take precedence)
        {"message": "make headers blue and add my experience at Apple", "expected_ui": False},
    ]
    
    print("🎨 Testing Advanced UI Agent Detection")
    print("=" * 60)
    
    correct_detections = 0
    total_tests = len(test_cases)
    
    for i, test in enumerate(test_cases, 1):
        message = test["message"]
        expected = test["expected_ui"]
        
        detected = agent.is_ui_modification_request(message)
        categories = agent.get_ui_modification_categories(message)
        
        status = "✅" if detected == expected else "❌"
        print(f"{status} Test {i:2d}: {message}")
        print(f"          Expected UI: {expected}, Detected: {detected}")
        if detected:
            print(f"          Categories: {categories}")
        print()
        
        if detected == expected:
            correct_detections += 1
    
    accuracy = (correct_detections / total_tests) * 100
    print(f"🎯 Detection Accuracy: {correct_detections}/{total_tests} ({accuracy:.1f}%)")
    
    # Test UI modification application
    print("\n🔧 Testing UI Modifications")
    print("=" * 60)
    
    ui_tests = [
        {"request": "make the name bold", "description": "Bold name formatting"},
        {"request": "use blue color for headers", "description": "Header color change"},
        {"request": "make layout more compact", "description": "Compact spacing"}
    ]
    
    for test in ui_tests:
        print(f"\n📝 Testing: {test['description']}")
        print(f"Request: '{test['request']}'")
        
        try:
            modified_resume = await agent.apply_ui_modifications(
                sample_resume, 
                test['request']
            )
            
            # Check if content integrity is maintained
            original_words = len([word for line in sample_resume.split('\n') 
                                for word in line.split() if word and not word.startswith('#')])
            modified_words = len([word for line in modified_resume.split('\n') 
                                for word in line.split() if word and not word.startswith('#')])
            
            word_preservation = abs(original_words - modified_words) <= 5  # Allow small variations
            
            # Check if basic structure is maintained  
            original_sections = len([line for line in sample_resume.split('\n') 
                                   if line.startswith('##')])
            modified_sections = len([line for line in modified_resume.split('\n') 
                                   if line.startswith('##')])
            
            structure_preserved = original_sections == modified_sections
            
            print(f"   Word count: {original_words} → {modified_words} ({'✅' if word_preservation else '❌'})")
            print(f"   Sections: {original_sections} → {modified_sections} ({'✅' if structure_preserved else '❌'})")
            
            if not word_preservation or not structure_preserved:
                print("   ⚠️  Potential content modification detected!")
            else:
                print("   ✅ Content integrity maintained")
                
        except Exception as e:
            print(f"   ❌ Error applying modification: {e}")
    
    print(f"\n🚀 Advanced UI Agent Test Complete!")
    print("Key Features:")
    print("- UI vs Content detection")
    print("- Content integrity protection") 
    print("- Category-based modification")
    print("- AI-powered styling changes")

if __name__ == "__main__":
    asyncio.run(test_ui_agent())