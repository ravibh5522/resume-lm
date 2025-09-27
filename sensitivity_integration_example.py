#!/usr/bin/env python3
"""
Simple Sensitivity Integration Example
Shows exactly how to integrate configurable sensitivity into your resume generator
"""

from sensitivity_control_panel import SensitivityControlPanel
from configurable_autofit_generator import ConfigurableAutoFitGenerator
import os

def create_custom_generator(sensitivity_level="balanced"):
    """
    Create a resume generator with your preferred sensitivity settings
    
    Args:
        sensitivity_level: 'conservative', 'balanced', or 'aggressive'
    
    Returns:
        Configured generator ready to use
    """
    
    # Create control panel
    control_panel = SensitivityControlPanel()
    
    # Load desired sensitivity profile
    control_panel.load_profile(sensitivity_level)
    
    # CUSTOMIZE THESE SETTINGS TO YOUR PREFERENCE:
    
    # Example 1: Make it more conservative (larger fonts, less scaling)
    if sensitivity_level == "conservative":
        control_panel.batch_adjust({
            'scaling_sensitivity': 0.6,          # Even less aggressive scaling
            'min_font_size': 8,                  # Don't go below 8pt
            'short_resume_lines': 35,            # Allow more lines before scaling
            'spacing_reduction': 0.95,           # Keep more spacing
        })
        print("🐌 Using EXTRA CONSERVATIVE settings")
    
    # Example 2: Make it more aggressive (smaller fonts, more scaling)  
    elif sensitivity_level == "aggressive":
        control_panel.batch_adjust({
            'scaling_sensitivity': 1.4,          # More aggressive scaling
            'min_font_size': 5,                  # Allow smaller fonts
            'short_resume_lines': 18,            # Start scaling earlier
            'spacing_reduction': 0.6,            # Reduce spacing more
        })
        print("🚀 Using EXTRA AGGRESSIVE settings")
    
    # Example 3: Custom balanced approach
    else:  # balanced
        control_panel.batch_adjust({
            'scaling_sensitivity': 1.1,          # Slightly more aggressive
            'min_font_size': 7,                  # Reasonable minimum
            'short_resume_lines': 22,            # Start scaling a bit earlier
            'spacing_reduction': 0.75,           # Moderate spacing reduction
        })
        print("⚖️ Using CUSTOM BALANCED settings")
    
    # Create and return the generator
    generator = control_panel.create_generator()
    return generator, control_panel

def test_different_sensitivities():
    """Test different sensitivity levels with the same resume"""
    
    # Sample resume for testing
    test_resume = """# Michael Chen
michael.chen@email.com | (555) 789-0123 | LinkedIn: linkedin.com/in/michael-chen
Portfolio: https://michaelchen.dev | GitHub: github.com/michaelchen | San Francisco, CA

## Professional Summary

**Senior Full-Stack Developer** with **8+ years** of experience building *scalable web applications* and **cloud infrastructure**. Expert in `JavaScript`, `Python`, **React**, and *AWS*. Led teams of **12+ engineers** and delivered projects worth **$15M+ in revenue**.

### Core Technical Skills
- **Frontend**: `React`, **Vue.js**, *Angular*, `TypeScript`, **HTML5/CSS3**
- **Backend**: `Node.js`, **Python**, *Django*, `Express`, **FastAPI**
- **Database**: `PostgreSQL`, **MongoDB**, *Redis*, `MySQL`, **Elasticsearch**
- **Cloud**: **AWS**, `Google Cloud`, *Azure*, `Docker`, **Kubernetes**

## Professional Experience

### Senior Full-Stack Developer
**Google | Mountain View, CA | 2020 - Present**

**Key Responsibilities:**
- Lead development of **cloud-native applications** serving `5M+ users daily`
- **Architecture**: Designed *microservices* infrastructure using **Docker** and `Kubernetes`
- **Team Leadership**: Mentor *8 junior developers* and conduct **technical interviews**
- **Performance**: Optimized systems achieving **99.9% uptime** and *<50ms response times*

**Major Achievements:**
- 🚀 **Innovation**: Built **real-time collaboration platform** using `WebSockets` and **Redis**
- 💰 **Business Impact**: Features delivered generated **$5M annual revenue increase**
- 🏆 **Recognition**: Won **"Technical Excellence Award 2023"** for *system architecture*
- 👥 **Team Growth**: Expanded engineering team from *6 to 14 members*

### Full-Stack Developer
**Stripe | San Francisco, CA | 2017 - 2020**

- Developed **payment processing APIs** handling `$500M+ transactions annually`
- **Technical Stack**: `Ruby on Rails`, **PostgreSQL**, *Redis*, `JavaScript`
- **Security**: Implemented **PCI DSS compliance** and *fraud detection algorithms*
- **Performance**: Reduced API latency by **60%** through *database optimization*

### Software Engineer
**Airbnb | San Francisco, CA | 2016 - 2017**

- Built **booking management system** for `2M+ property listings`
- **Frontend**: Developed *responsive interfaces* using **React** and `Redux`
- **Backend**: Created **RESTful APIs** using `Node.js` and *Express*

## Education

### Master of Science in Computer Science
**Stanford University | Stanford, CA | 2014 - 2016**
- **Specialization**: *Distributed Systems* and **Machine Learning**
- **Thesis**: "Scalable Real-time Data Processing Architecture"
- **GPA**: 3.8/4.0

### Bachelor of Science in Software Engineering
**UC Berkeley | Berkeley, CA | 2010 - 2014**
- **Magna Cum Laude** with *Computer Science* concentration
- **Activities**: *ACM Programming Contest* winner, **Open Source contributor**

## Key Projects

### 🌟 Real-Time Analytics Platform
**Role**: *Technical Lead* | **Duration**: 18 months | **Team**: 10 engineers
- **Description**: Built comprehensive **data visualization platform** processing `10TB+ daily`
- **Technologies**: `React`, **D3.js**, *Node.js*, `Apache Kafka`, **ClickHouse**
- **Impact**: **250% improvement** in data processing speed, *$2M cost savings*

### 🔒 Security Monitoring System
**Role**: **Senior Developer** | **Duration**: 12 months | **Team**: 6 engineers
- **Description**: Developed *threat detection system* with **ML-powered anomaly detection**
- **Technologies**: `Python`, **TensorFlow**, *Elasticsearch*, `Kubernetes`
- **Results**: **95% threat detection accuracy**, *reduced incidents by 70%*

## Certifications & Awards

### Professional Certifications
- **AWS Solutions Architect Professional** (2023)
- *Google Cloud Professional Developer* (2022)
- **Kubernetes Certified Application Developer** (2021)
- *Scrum Master Certified* (2020)

### Recognition
- 🏆 **"Innovator of the Year"** - Google (2023)
- 🌟 *"Outstanding Technical Contribution"* - Stripe (2019)
- 🎯 **"Best Software Design"** - Airbnb (2017)"""

    print("🧪 TESTING DIFFERENT SENSITIVITY LEVELS")
    print("=" * 70)
    
    sensitivity_levels = ['conservative', 'balanced', 'aggressive']
    
    for level in sensitivity_levels:
        print(f"\n🎛️ Testing {level.upper()} sensitivity:")
        print("-" * 40)
        
        try:
            # Create generator with this sensitivity level
            generator, control_panel = create_custom_generator(level)
            
            # Show the settings being used
            lines = len([line for line in test_resume.split('\n') if line.strip()])
            words = len(test_resume.split())
            chars = len(test_resume)
            
            print(f"📊 Test resume: {lines} lines, {words} words, {chars:,} characters")
            
            # Generate the DOCX
            result = generator.generate_configurable_docx_base64(test_resume)
            print(f"✅ Generated: {len(result):,} characters")
            
        except Exception as e:
            print(f"❌ Failed: {e}")
    
    print(f"\n🎉 Sensitivity testing complete!")

def main():
    """Main function demonstrating usage"""
    
    print("🎛️ CONFIGURABLE AUTO-FIT SENSITIVITY DEMO")
    print("=" * 60)
    
    print("📋 This demo shows you exactly how to:")
    print("   1. Create generators with different sensitivity levels")
    print("   2. Customize the sensitivity parameters") 
    print("   3. Test with real resume content")
    print("   4. Choose the best settings for your needs")
    
    # Test different sensitivity levels
    test_different_sensitivities()
    
    print(f"\n💡 TO USE IN YOUR MAIN APPLICATION:")
    print("=" * 50)
    print("""
# Replace your current generator initialization with:

from sensitivity_control_panel import SensitivityControlPanel

# Create control panel and customize
control_panel = SensitivityControlPanel()
control_panel.load_profile('balanced')  # or 'conservative' or 'aggressive'

# Fine-tune settings (ADJUST THESE TO YOUR PREFERENCE):
control_panel.batch_adjust({
    'scaling_sensitivity': 1.1,     # How aggressive: 0.5 (gentle) to 2.0 (aggressive)
    'min_font_size': 7,             # Minimum font size: 5-10pt
    'short_resume_lines': 22,       # When to start scaling: 15-35 lines
    'spacing_reduction': 0.75,      # Spacing: 0.5 (tight) to 1.0 (loose)
})

# Create your generator
pdf_generator = control_panel.create_generator()  # Returns ConfigurableAutoFitGenerator
docx_generator = control_panel.create_generator() # Use same for both or create separate

# Use in your endpoints exactly like before:
pdf_result = pdf_generator.generate_configurable_pdf_base64(markdown)
docx_result = docx_generator.generate_configurable_docx_base64(markdown)
""")

if __name__ == "__main__":
    main()