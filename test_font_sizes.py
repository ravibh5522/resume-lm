#!/usr/bin/env python3
"""
Test font sizes with short vs long resumes
"""

from main import pdf_only_generator, docx_generator

def test_font_sizes():
    print("🧪 TESTING FONT SIZES WITH DIFFERENT CONTENT LENGTHS")
    print("=" * 60)
    
    # SHORT RESUME (should have LARGE fonts)
    short_resume = """# John Smith
john.smith@email.com | (555) 123-4567 | Boston, MA

## Professional Summary

**Software Developer** with **3+ years** of experience in *web development*.

## Experience

### Software Developer
**TechCorp | Boston, MA | 2021 - Present**

- Built web applications using `JavaScript` and **React**
- Collaborated with team of **5 developers**
- **Key Achievement**: Improved app performance by *25%*

## Education

**Bachelor of Computer Science**
*Boston University | Boston, MA | 2017 - 2021*

## Skills

**Programming:** `JavaScript`, **Python**, `React`, **Node.js**"""

    # LONG RESUME (should have smaller fonts)
    long_resume = """# Sarah Johnson
sarah.johnson@email.com | (555) 987-6543 | San Francisco, CA

## Professional Summary

**Senior Software Engineer** with **8+ years** of experience developing *scalable web applications* and **cloud infrastructure**. Expert in `JavaScript`, **Python**, `React`, **AWS**, and *DevOps practices*. Led teams of **15+ engineers** and delivered projects worth **$20M+ in revenue**.

## Experience

### Senior Software Engineer
**Google | Mountain View, CA | 2019 - Present**

- Lead development of **cloud-native applications** serving `10M+ users`
- **Architecture**: Designed *microservices* using **Docker** and `Kubernetes`
- **Team Leadership**: Mentor *12 junior developers*
- **Performance**: Achieved **99.99% uptime** and *<30ms response times*
- **Innovation**: Built **real-time collaboration platform**
- **Business Impact**: Features generated **$8M annual revenue**

### Software Engineer
**Facebook | Menlo Park, CA | 2016 - 2019**

- Developed **social media features** used by `2B+ users daily`
- **Tech Stack**: `React`, **GraphQL**, *Node.js*, `PostgreSQL`
- **Security**: Implemented **OAuth2** and *data encryption*
- **Performance**: Reduced load times by **45%**
- **Collaboration**: Worked with **product managers** and *designers*

### Junior Developer
**Startup Inc | San Francisco, CA | 2015 - 2016**

- Built **e-commerce platform** handling `$5M+ transactions`
- **Frontend**: Created responsive interfaces using **React**
- **Backend**: Developed APIs using `Node.js` and *Express*

## Education

### Master of Computer Science
**Stanford University | Stanford, CA | 2013 - 2015**
- **Specialization**: *Distributed Systems* and **Machine Learning**
- **Thesis**: "Real-time Data Processing at Scale"
- **GPA**: 3.9/4.0

### Bachelor of Software Engineering
**UC Berkeley | Berkeley, CA | 2009 - 2013**
- **Magna Cum Laude** with *Computer Science* focus
- **Activities**: *Programming Contest* winner

## Projects

### Real-Time Analytics Platform
**Role**: *Technical Lead* | **Duration**: 24 months
- Built **data visualization platform** processing `50TB+ daily`
- **Technologies**: `React`, **D3.js**, *Apache Kafka*
- **Impact**: **300% improvement** in processing speed

### AI-Powered Recommendation Engine
**Role**: **Lead Developer** | **Duration**: 18 months
- Developed *machine learning system* with **95% accuracy**
- **Technologies**: `Python`, **TensorFlow**, *Docker*
- **Results**: **40% increase** in user engagement

## Certifications

- **AWS Solutions Architect Professional** (2023)
- *Google Cloud Professional Developer* (2022)
- **Kubernetes Application Developer** (2021)

## Skills

**Languages**: `JavaScript`, **Python**, *Java*, `Go`, **TypeScript**
**Frameworks**: **React**, `Vue.js`, *Angular*, `Django`, **FastAPI**
**Databases**: `PostgreSQL`, **MongoDB**, *Redis*, `Elasticsearch`
**Cloud**: **AWS**, `Google Cloud`, *Azure*, `Docker`, **Kubernetes**"""

    print("\n📏 SHORT RESUME TEST (should use LARGE fonts):")
    print("-" * 50)
    
    # Count lines in short resume
    short_lines = len([line for line in short_resume.split('\n') if line.strip()])
    print(f"📊 Short resume: {short_lines} content lines, {len(short_resume)} characters")
    
    try:
        # Test PDF generation
        pdf_result = pdf_only_generator.generate_auto_fit_pdf_base64(short_resume)
        print(f"✅ SHORT PDF: Generated successfully ({len(pdf_result)} chars)")
        
        # Test DOCX generation  
        docx_result = docx_generator.generate_configurable_docx_base64(short_resume)
        print(f"✅ SHORT DOCX: Generated successfully ({len(docx_result)} chars)")
        
    except Exception as e:
        print(f"❌ SHORT resume failed: {e}")
    
    print("\n📏 LONG RESUME TEST (should use smaller fonts):")
    print("-" * 50)
    
    # Count lines in long resume
    long_lines = len([line for line in long_resume.split('\n') if line.strip()])
    print(f"📊 Long resume: {long_lines} content lines, {len(long_resume)} characters")
    
    try:
        # Test PDF generation
        pdf_result = pdf_only_generator.generate_auto_fit_pdf_base64(long_resume)
        print(f"✅ LONG PDF: Generated successfully ({len(pdf_result)} chars)")
        
        # Test DOCX generation
        docx_result = docx_generator.generate_configurable_docx_base64(long_resume)
        print(f"✅ LONG DOCX: Generated successfully ({len(docx_result)} chars)")
        
    except Exception as e:
        print(f"❌ LONG resume failed: {e}")
    
    print(f"\n💡 EXPECTED BEHAVIOR:")
    print(f"   📏 Short resume ({short_lines} lines): Should use NORMAL size fonts (no scaling)")
    print(f"   📏 Long resume ({long_lines} lines): Should use smaller fonts (scaling applied)")
    print(f"   🎯 This ensures short resumes don't have tiny fonts!")

if __name__ == "__main__":
    test_font_sizes()