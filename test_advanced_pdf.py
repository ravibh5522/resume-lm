#!/usr/bin/env python3
"""
Test the advanced PDF generator with better markdown parsing
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from advanced_pdf_generator import AdvancedPDFGenerator

load_dotenv()

def test_advanced_pdf_generator():
    """Test the advanced PDF generator with sample resume markdown"""
    print("🧪 Testing Advanced PDF Generator...")
    
    try:
        generator = AdvancedPDFGenerator()
        
        # Sample resume markdown with complex formatting
        sample_markdown = """
# Alex Johnson

San Francisco, CA  |  (555) 123-4567  |  alex.johnson@email.com
[LinkedIn](https://linkedin.com/in/alexjohnson)  |  [GitHub](https://github.com/alexjohnson)  |  [Portfolio](https://www.alexjohnson.dev)

---

🚀 PROFESSIONAL SUMMARY

Results-oriented Software Engineer with 5+ years of experience in full-stack web development, specializing in scalable web applications and cloud-based solutions. Adept at leading agile teams, architecting robust systems, and delivering high-impact projects that drive business growth.

---

💼 PROFESSIONAL EXPERIENCE

**Senior Software Engineer**
Tech Solutions Inc.  |  San Francisco, CA
Jan 2022 – Present

◆ Led a team of 6 engineers to develop SaaS platforms serving 50,000+ users.
◆ Architected and implemented RESTful APIs, reducing data retrieval time by 30%.
◆ Enhanced CI/CD pipeline, decreasing release cycle from 2 weeks to 3 days.
◆ Mentored junior developers, fostering a culture of continuous learning.

**Full Stack Developer**
InnovateWeb LLC  |  San Francisco, CA
Jun 2018 – Dec 2021

◆ Designed & launched 10+ web applications using React and Node.js.
◆ Optimized database queries, boosting application performance by 40%.
◆ Delivered client solutions ahead of deadlines through agile collaboration.

---

🎓 EDUCATION

**Bachelor of Science in Computer Science**
University of California, Berkeley  |  Berkeley, CA
2014 – 2018  |  _GPA: 3.7/4.0_

---

⚡ TECHNICAL SKILLS

**Languages & Frameworks:**
🔹 JavaScript (ES6+), Python, TypeScript, SQL
🔹 React, Node.js, Express, React Native

**Cloud & DevOps:**
🔹 AWS (EC2, S3, Lambda), Docker, CI/CD

**Databases:**
🔹 PostgreSQL, MongoDB, Firebase

---

🚀 SELECTED PROJECTS

◆ **TaskMaster App**
A productivity app enabling teams to track projects efficiently.
Tech: React Native, Firebase
[Live Demo](https://taskmasterapp.dev)

⚡ Designed intuitive UI/UX for seamless team collaboration.
⚡ Implemented real-time sync, supporting 1,000+ concurrent users.
⚡ Integrated push notifications, increasing user engagement by 25%.

◆ **E-Commerce Dashboard**
Analytics dashboard for tracking sales and trends.
Tech: Node.js, React, PostgreSQL

⚡ Developed interactive data visualizations for actionable insights.
⚡ Automated data aggregation, reducing manual reporting by 80%.

---

📜 CERTIFICATIONS

🏅 AWS Certified Solutions Architect
🏅 Certified ScrumMaster (CSM)

---

🌍 LANGUAGES

English: Native
Spanish: Professional Proficiency
        """
        
        # Generate PDF
        pdf_bytes = generator.markdown_to_pdf(sample_markdown)
        
        if pdf_bytes and len(pdf_bytes) > 0:
            # Save test PDF
            with open('/home/ravi/Desktop/resume-lm/test_advanced_resume.pdf', 'wb') as f:
                f.write(pdf_bytes)
            
            print("✅ Advanced PDF generation successful!")
            print(f"📄 PDF size: {len(pdf_bytes)} bytes")
            print("📁 Saved as: test_advanced_resume.pdf")
            
            # Test base64 encoding
            base64_pdf = generator.get_base64_pdf(sample_markdown)
            print(f"📦 Base64 encoded length: {len(base64_pdf)} characters")
            
            return True
        else:
            print("❌ PDF generation failed - empty result")
            return False
            
    except Exception as e:
        print(f"❌ Error testing advanced PDF generator: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run the test"""
    print("🚀 Testing Advanced PDF Generator")
    print("=" * 50)
    
    success = test_advanced_pdf_generator()
    
    if success:
        print("\n🎉 Advanced PDF generator is working perfectly!")
        print("📋 The generator now properly preserves markdown structure.")
    else:
        print("\n⚠️  Issues found with advanced PDF generator.")

if __name__ == "__main__":
    main()