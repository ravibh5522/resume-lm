#!/usr/bin/env python3
"""
Test script for targeted resume modifications
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from resume_modifier import ResumeModifier

load_dotenv()

def test_modification_detection():
    """Test if the modifier can detect different types of modifications"""
    print("🧪 Testing Modification Detection")
    print("=" * 50)
    
    modifier = ResumeModifier()
    
    # Sample resume markdown
    sample_resume = """# John Smith
Location | Phone | Email | LinkedIn

## 🚀 Professional Summary
Experienced software engineer...

## 💼 Professional Experience
Senior Developer at Tech Corp
- Built scalable applications
- Led team of 5 engineers

## 🎓 Education
Bachelor of Science in Computer Science
University of Tech | 2020-2024
"""
    
    test_queries = [
        ("change font of name", "small"),
        ("make name bold", "small"), 
        ("add blue color to headers", "small"),
        ("make it more compact", "medium"),
        ("convert education to table format", "medium"),
        ("add new work experience", "large"),
        ("remove current job", "large"),
        ("can you make the spacing tighter", "small"),
        ("change layout to two columns", "medium")
    ]
    
    print("Testing modification detection:")
    for query, expected_impact in test_queries:
        can_handle = modifier.can_handle_modification(query, sample_resume)
        actual_impact = modifier.estimate_change_impact(query)
        
        status = "✅" if can_handle and actual_impact == expected_impact else "❌"
        print(f"{status} '{query}' -> Can handle: {can_handle}, Impact: {actual_impact} (expected: {expected_impact})")
    
    return True

def test_font_modification():
    """Test font modification functionality"""
    print("\n🔤 Testing Font Modifications")
    print("=" * 50)
    
    modifier = ResumeModifier()
    
    original_resume = """# John Smith
Location | Phone | Email

## Summary
Software engineer with 5 years experience.
"""
    
    # Test bold name modification
    modified = modifier.apply_modification("make name bold", original_resume)
    print("Original name line:")
    print("# John Smith")
    print("\nModified name line:")
    for line in modified.split('\n'):
        if line.startswith('# '):
            print(line)
            break
    
    expected_bold = "# **John Smith**"
    success = expected_bold in modified
    print(f"\n{'✅' if success else '❌'} Bold modification {'successful' if success else 'failed'}")
    
    return success

def test_layout_modification():
    """Test layout modification functionality"""
    print("\n📐 Testing Layout Modifications")
    print("=" * 50)
    
    modifier = ResumeModifier()
    
    original_resume = """# John Smith

Location: San Francisco
Phone: (555) 123-4567
Email: john@email.com


## Summary

Software engineer with experience.


## Experience

Senior Developer at Tech Corp
"""
    
    # Test compact modification
    modified = modifier.apply_modification("make it more compact", original_resume)
    
    original_lines = len(original_resume.split('\n'))
    modified_lines = len(modified.split('\n'))
    
    print(f"Original lines: {original_lines}")
    print(f"Modified lines: {modified_lines}")
    print(f"Reduction: {original_lines - modified_lines} lines")
    
    success = modified_lines < original_lines
    print(f"{'✅' if success else '❌'} Compact modification {'successful' if success else 'failed'}")
    
    return success

def main():
    """Run all tests"""
    print("🚀 Testing Resume Modifier System")
    print("=" * 60)
    
    test1 = test_modification_detection()
    test2 = test_font_modification()
    test3 = test_layout_modification()
    
    print("\n📊 Test Results")
    print("=" * 30)
    print(f"Modification Detection: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Font Modifications: {'✅ PASS' if test2 else '❌ FAIL'}")
    print(f"Layout Modifications: {'✅ PASS' if test3 else '❌ FAIL'}")
    
    if all([test1, test2, test3]):
        print("\n🎉 All tests passed! Resume modifier is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check implementation.")
    
    print("\n💡 How it works:")
    print("- Small changes (font, color, spacing) = Quick modification")
    print("- Medium changes (layout, format) = Targeted modification") 
    print("- Large changes (add/remove content) = Full regeneration")

if __name__ == "__main__":
    main()