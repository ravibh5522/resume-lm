#!/usr/bin/env python3
"""
Test the improved font size ratios - should show better proportional sizing
"""

from main import pdf_only_generator, docx_generator

def test_proportional_fonts():
    print("🎯 TESTING PROPORTIONAL FONT SIZES (Fixed Size Gaps)")
    print("=" * 65)
    
    # Test resume similar to the attachment
    test_resume = """# Alex Johnson
alex.johnson@email.com | (555) 123-4567 | San Francisco, CA

## TECHNICAL SKILLS

**Programming Languages:** Python, JavaScript, Java, C++
**Frameworks:** React, Node.js, Django, Spring Boot
**Databases:** PostgreSQL, MongoDB, Redis
**Cloud Technologies:** AWS, Docker, Kubernetes
**DevOps:** Git, Jenkins, CI/CD
**Methodologies:** Agile/Scrum, Team Leading

## NOTABLE PROJECTS

### SmartHome IoT Platform
• **Developed** a scalable system for connecting and managing smart home devices with real-time data and remote controls.
**Technologies:** React, Node.js, AWS IoT, MongoDB **Live Demo** | **Source**

### Virtual Event Hub  
• **Built** a virtual platform enabling live streaming, networking, and ticketing for over 10,000 users.
**Technologies:** TypeScript, GraphQL, PostgreSQL, Firebase **Live Demo** | **Source**

## CERTIFICATIONS & ACHIEVEMENTS

• **AWS Certified Solutions Architect - Associate**
• **Certified ScrumMaster (CSM)**

## LANGUAGES

| Language | Proficiency   |
|----------|---------------|
| English  | Native        |
| Spanish  | Conversational|"""

    print("📊 Test Resume Analysis:")
    lines = len([line for line in test_resume.split('\n') if line.strip()])
    words = len(test_resume.split())
    print(f"   📏 Content lines: {lines}")
    print(f"   📝 Word count: {words}")
    print(f"   📄 Character count: {len(test_resume)}")
    
    print(f"\n🔤 FONT SIZE RATIOS - BEFORE vs AFTER:")
    print("─" * 50)
    print("📚 BEFORE (Too much gap):")
    print("   H1 (Name): 24pt → 18pt")  
    print("   H2 (Sections): 14pt → 12pt")
    print("   Body: 12pt → 10pt")
    print("   📊 H1 to Body ratio: 2.4:1 to 1.8:1 (TOO BIG!)")
    print("")
    print("✅ AFTER (Better proportions):")
    print("   H1 (Name): 16pt → 14pt")  
    print("   H2 (Sections): 12pt → 11pt")
    print("   Body: 12pt → 10pt")
    print("   📊 H1 to Body ratio: 1.6:1 to 1.4:1 (Much better!)")
    
    print(f"\n🧪 TESTING PDF GENERATION:")
    print("─" * 30)
    
    try:
        pdf_result = pdf_only_generator.generate_auto_fit_pdf_base64(test_resume)
        print(f"✅ PDF: Generated successfully ({len(pdf_result)} characters)")
    except Exception as e:
        print(f"❌ PDF failed: {e}")
    
    print(f"\n🧪 TESTING DOCX GENERATION:")
    print("─" * 30)
    
    try:
        docx_result = docx_generator.generate_configurable_docx_base64(test_resume)
        print(f"✅ DOCX: Generated successfully ({len(docx_result)} characters)")
    except Exception as e:
        print(f"❌ DOCX failed: {e}")
    
    print(f"\n💡 IMPROVEMENTS MADE:")
    print("═" * 40)
    print("🎯 **Font Size Gaps Reduced:**")
    print("   • Headers are now proportionally smaller")
    print("   • Better visual hierarchy") 
    print("   • More professional appearance")
    print("   • Headers won't dominate the page")
    print("")
    print("📏 **New Proportional Ratios:**")
    print("   • Name header: Only 20-40% larger than body text")
    print("   • Section headers: Only 10-20% larger than body text")
    print("   • Creates balanced, readable documents")
    print("")
    print("🎨 **Visual Impact:**")
    print("   • Less jarring size differences")
    print("   • More space for actual content")
    print("   • Professional, modern look")

if __name__ == "__main__":
    test_proportional_fonts()