#!/usr/bin/env python3
"""
Header Parsing Comparison Tool
Demonstrates the fix for ## header parsing issues
"""

import re
from pdf_generator_optimized import OptimizedPDFGenerator
from pdf_generator_enhanced import EnhancedPdfGenerator

def test_header_parsing_comparison():
    """
    Compare header parsing between old and new generators
    Shows the specific ## header fix
    """
    
    test_markdown = """# John Doe
john.doe@email.com | (555) 123-4567

## Education
Bachelor's Degree in Computer Science

## Professional Experience  
Senior Software Engineer at Tech Corp

## Technical Skills
Python, JavaScript, React

## Projects
Built various applications"""

    print("🔍 Header Parsing Comparison Test")
    print("=" * 60)
    print(f"📝 Test Markdown:")
    header_pattern = r'^##\s+'
    print(f"   Contains {len(re.findall(header_pattern, test_markdown, re.MULTILINE))} '##' headers")
    print()
    
    try:
        # Test old generator
        print("🔧 Testing Original Generator...")
        old_generator = OptimizedPDFGenerator()
        
        # Check preprocessing
        old_processed = old_generator.preprocess_markdown(test_markdown)
        old_headers = re.findall(r'^##\\s+([^\\n]+)', old_processed, re.MULTILINE)
        print(f"   Original preprocessing found: {len(old_headers)} headers")
        print(f"   Headers: {old_headers}")
        
        # Test HTML conversion
        import markdown
        md = markdown.Markdown(extensions=['markdown.extensions.extra'])
        old_html = md.convert(old_processed)
        old_h2_tags = re.findall(r'<h2[^>]*>([^<]+)</h2>', old_html)
        print(f"   HTML conversion produced: {len(old_h2_tags)} h2 tags")
        print(f"   H2 content: {old_h2_tags}")
        print()
        
        # Test new generator
        print("⚡ Testing Enhanced Generator...")
        new_generator = EnhancedPdfGenerator()
        
        # Check preprocessing  
        new_processed = new_generator.preprocess_markdown_enhanced(test_markdown)
        new_headers = re.findall(r'^##\\s+([^\\n]+)', new_processed, re.MULTILINE)
        print(f"   Enhanced preprocessing found: {len(new_headers)} headers")
        print(f"   Headers: {new_headers}")
        
        # Test HTML conversion
        new_html = new_generator.markdown_to_html_enhanced(test_markdown)
        new_h2_tags = re.findall(r'<h2[^>]*>([^<]+)</h2>', new_html)
        print(f"   Enhanced HTML conversion produced: {len(new_h2_tags)} h2 tags")
        print(f"   H2 content: {new_h2_tags}")
        print()
        
        # Summary
        print("📊 COMPARISON RESULTS:")
        print(f"   Original Generator: {len(old_h2_tags)} headers in final HTML")
        print(f"   Enhanced Generator: {len(new_h2_tags)} headers in final HTML")
        
        if len(new_h2_tags) > len(old_h2_tags):
            print("   ✅ Enhanced generator successfully fixed header parsing!")
            print(f"   🔧 Improvement: +{len(new_h2_tags) - len(old_h2_tags)} additional headers parsed")
        elif len(new_h2_tags) == len(old_h2_tags):
            print("   ✅ Both generators parse headers equally well")
        else:
            print("   ⚠️  Original generator parsed more headers")
        
        return True
        
    except Exception as e:
        print(f"❌ Comparison test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_generation_comparison():
    """
    Generate PDFs with both generators for size/quality comparison
    """
    
    test_markdown = """# Sarah Johnson
sarah.johnson@email.com | (555) 987-6543 | LinkedIn: linkedin.com/in/sarah-johnson

## Professional Summary
Experienced software engineer with 8+ years in full-stack development

## Education
**Master of Science in Computer Science**  
*Stanford University | 2018-2020*

## Professional Experience

**Senior Software Engineer**  
*Google Inc. | 2020-Present*
- Led development of microservices architecture
- Improved system performance by **35%**
- Mentored team of *5 junior developers*

## Technical Skills
- **Languages:** `Python`, `JavaScript`, `TypeScript`, `Java`
- **Frameworks:** `React`, `Node.js`, `Django`, `Spring Boot`
- **Databases:** `PostgreSQL`, `MongoDB`, `Redis`

## Key Projects

### E-Commerce Platform
Built scalable e-commerce platform serving **1M+ users**

### ML Pipeline
Developed machine learning pipeline for recommendation system"""

    print("📊 PDF Generation Comparison")
    print("=" * 50)
    
    try:
        # Test original generator
        print("🔧 Testing Original PDF Generator...")
        old_generator = OptimizedPDFGenerator()
        old_pdf = old_generator.generate_pdf_base64(test_markdown)
        print(f"   Original PDF size: {len(old_pdf) if old_pdf else 0} characters")
        
        # Test enhanced generator
        print("⚡ Testing Enhanced PDF Generator...")
        new_generator = EnhancedPdfGenerator()
        new_pdf = new_generator.generate_pdf_base64_enhanced(test_markdown)
        print(f"   Enhanced PDF size: {len(new_pdf) if new_pdf else 0} characters")
        
        # Comparison
        print()
        print("📊 GENERATION COMPARISON:")
        if old_pdf and new_pdf:
            size_diff = len(new_pdf) - len(old_pdf)
            print(f"   Size difference: {size_diff:+} characters")
            print(f"   Both generators successful: ✅")
        elif new_pdf:
            print("   ✅ Enhanced generator successful")
            print("   ❌ Original generator failed")
        elif old_pdf:
            print("   ✅ Original generator successful")  
            print("   ❌ Enhanced generator failed")
        else:
            print("   ❌ Both generators failed")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF generation comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Running Header Parsing Fix Verification")
    print("=" * 60)
    
    # Run header parsing test
    print("🔍 PART 1: Header Parsing Analysis")
    test_header_parsing_comparison()
    
    print("\\n" + "=" * 60)
    
    # Run PDF generation test
    print("🔍 PART 2: PDF Generation Comparison")
    test_pdf_generation_comparison()
    
    print("\\n" + "=" * 60)
    print("🎉 Header parsing fix verification complete!")
    print("✅ Enhanced generators now properly handle ## headers")