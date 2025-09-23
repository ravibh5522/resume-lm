#!/usr/bin/env python3
"""
Debug script for resume modification system
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resume_modifier import ResumeModifier

load_dotenv()

def test_modification_detection():
    """Test modification detection logic"""
    print("🧪 Testing Modification Detection")
    print("=" * 50)
    
    modifier = ResumeModifier()
    
    test_cases = [
        "can you change font of name please",
        "make the name bold",
        "add blue color to headers",
        "make it more compact",
        "add my work experience at Microsoft",
        "change my email address",
        "update my phone number",
        "make the spacing tighter"
    ]
    
    for message in test_cases:
        is_quick = modifier.is_quick_modification(message)
        impact = modifier.estimate_change_impact(message)
        print(f"📝 '{message}'")
        print(f"   ⚡ Quick mod: {is_quick}")
        print(f"   🎯 Impact: {impact}")
        print()

def test_modification_application():
    """Test actual modification application"""
    print("\n🔧 Testing Modification Application")
    print("=" * 50)
    
    modifier = ResumeModifier()
    
    sample_resume = """# John Doe
Location | Phone | Email | LinkedIn | GitHub

## Professional Summary
Software engineer with 5 years of experience.

## Experience
### Senior Developer
**Google** | 2020-Present
- Built scalable systems
- Led team of 5 engineers
"""
    
    test_modifications = [
        "make the name bold",
        "change font of name",
        "make it more compact"
    ]
    
    for modification in test_modifications:
        print(f"🔄 Testing: '{modification}'")
        result = modifier.apply_modification(modification, sample_resume)
        print(f"📄 Result length: {len(result)} chars")
        if result != sample_resume:
            print("✅ Modification applied")
            print(f"📝 Changes detected in first 200 chars:")
            print(f"Before: {sample_resume[:200]}...")
            print(f"After:  {result[:200]}...")
        else:
            print("❌ No changes applied")
        print()

if __name__ == "__main__":
    test_modification_detection()
    test_modification_application()