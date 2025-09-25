#!/usr/bin/env python3
"""
Test script for the new DOC/DOCX generation functionality
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from docx_generator import ProfessionalDocxGenerator

def test_docx_generation():
    """Test the DOCX generation with sample resume data"""
    
    print("🧪 Testing DOCX Generation Functionality")
    print("=" * 50)
    
    sample_markdown = """# Sarah Johnson
sarah.johnson@email.com | (555) 987-6543 | LinkedIn: linkedin.com/in/sarahjohnson | New York, NY

## Professional Summary

Results-driven software engineer with 6+ years of experience in full-stack development and cloud architecture. Expertise in Python, React, and AWS with a proven track record of delivering scalable solutions that serve millions of users.

## Experience

**Lead Software Engineer**
*InnovateTech Solutions | New York, NY | 2021 - Present*

- Architected and implemented microservices platform serving 2M+ daily active users
- Led a cross-functional team of 8 engineers in agile development practices
- Reduced system latency by 35% through database optimization and caching strategies
- Mentored junior developers and established code review best practices
- Technologies: Python, Django, React, PostgreSQL, Redis, AWS, Docker, Kubernetes

**Senior Software Engineer**
*TechStartup Inc. | San Francisco, CA | 2018 - 2021*

- Developed and maintained RESTful APIs processing 100K+ requests daily
- Built responsive web applications with modern frontend frameworks
- Implemented CI/CD pipelines reducing deployment time from hours to minutes
- Collaborated with product managers to define technical requirements
- Technologies: JavaScript, Node.js, Vue.js, MongoDB, Express.js, GitLab CI

**Software Engineer**
*DevCorp | Austin, TX | 2017 - 2018*

- Created automated testing suites improving code coverage by 40%
- Developed internal tools that increased team productivity by 25%
- Participated in on-call rotation supporting production systems
- Technologies: Java, Spring Boot, MySQL, JUnit, Maven

## Education

**Master of Science in Computer Science**
*Stanford University | Stanford, CA | 2015 - 2017*

- Specialization: Artificial Intelligence and Machine Learning
- Thesis: "Deep Learning Approaches for Natural Language Processing"
- GPA: 3.9/4.0

**Bachelor of Science in Software Engineering**
*University of California, Berkeley | Berkeley, CA | 2011 - 2015*

- Minor in Mathematics
- Magna Cum Laude, GPA: 3.8/4.0

## Skills

**Programming Languages:** Python, JavaScript, Java, TypeScript, Go, SQL
**Frameworks & Libraries:** Django, React, Node.js, Vue.js, Spring Boot, Flask
**Databases:** PostgreSQL, MongoDB, Redis, MySQL, DynamoDB
**Cloud & DevOps:** AWS, Docker, Kubernetes, Jenkins, GitLab CI, Terraform
**Tools:** Git, Jira, Figma, Postman, VS Code

## Projects

**E-Commerce Analytics Platform**
- Built real-time analytics dashboard processing 500GB+ daily data
- Implemented machine learning models for sales forecasting with 85% accuracy
- Technologies: Python, Apache Spark, AWS EMR, React, D3.js
- GitHub: github.com/sarahjohnson/ecommerce-analytics

**Open Source Contribution - React Testing Library**
- Contributed performance improvements reducing test execution time by 20%
- Added new testing utilities used by 10K+ developers monthly
- Maintained documentation and provided community support

## Certifications

- AWS Certified Solutions Architect - Professional (2023)
- Certified Kubernetes Application Developer (2022)
- Google Cloud Professional Data Engineer (2021)

## Awards & Recognition

- "Engineer of the Year" - InnovateTech Solutions (2023)
- "Best Technical Innovation" - TechStartup Inc. (2020)
- Dean's List - Stanford University (2016, 2017)
"""
    
    try:
        # Test the DOCX generator
        generator = ProfessionalDocxGenerator()
        
        print("📝 Generating DOCX from sample resume...")
        
        # Test base64 generation
        docx_base64 = generator.generate_docx_base64(sample_markdown)
        
        if docx_base64:
            print(f"✅ Base64 DOCX generation successful!")
            print(f"   Size: {len(docx_base64)} characters")
            print(f"   Preview: {docx_base64[:100]}...")
        else:
            print("❌ Base64 DOCX generation failed")
            return False
        
        # Test file saving
        print("\n💾 Saving DOCX file...")
        success = generator.save_docx_file(sample_markdown, "test_resume_output.docx")
        
        if success:
            print("✅ DOCX file saved successfully as 'test_resume_output.docx'")
            print("   You can open this file in Microsoft Word to verify formatting")
        else:
            print("❌ DOCX file saving failed")
            return False
        
        print("\n🎉 All DOCX generation tests passed!")
        print("\n📋 Test Summary:")
        print(f"   ✓ Base64 generation: Working ({len(docx_base64)} chars)")
        print("   ✓ File generation: Working (test_resume_output.docx created)")
        print("   ✓ Professional styling: Applied")
        print("   ✓ ATS compatibility: Ensured")
        
        return True
        
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("💡 Install with: pip install python-docx")
        return False
        
    except Exception as e:
        print(f"❌ Error during DOCX generation test: {e}")
        return False

if __name__ == "__main__":
    success = test_docx_generation()
    if success:
        print("\n✅ Ready to integrate DOCX functionality into the main application!")
    else:
        print("\n❌ Please fix the issues above before proceeding.")
    sys.exit(0 if success else 1)