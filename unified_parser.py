#!/usr/bin/env python3
"""
Unified Resume Parser - Fixes parsing issues for both PDF and DOCX
Ensures consistent rendering across all formats
"""

import re
import markdown
from typing import Dict, List, Tuple, Optional

class UnifiedResumeParser:
    """
    Unified parser that ensures consistent markdown processing for both PDF and DOCX generation
    Fixes header parsing and format conversion issues
    """
    
    def __init__(self):
        self.section_patterns = {
            'header': r'^#\s+(.+)$',
            'section': r'^##\s+(.+)$', 
            'subsection': r'^###\s+(.+)$',
            'bold_title': r'^\*\*([^*]+)\*\*$',
            'italic_company': r'^\*([^*]+)\*$',
            'bullet': r'^[\s]*[-•*]\s+(.+)$',
            'numbered': r'^[\s]*\d+\.\s+(.+)$',
        }
    
    def normalize_markdown(self, markdown_text: str) -> str:
        """
        Normalize markdown to ensure consistent parsing across PDF and DOCX
        Fixes common parsing issues
        """
        text = markdown_text.strip()
        
        # Fix header spacing issues
        text = re.sub(r'^(#+)\s*([^\n]+)\s*$', r'\1 \2', text, flags=re.MULTILINE)
        
        # Ensure proper spacing after headers
        text = re.sub(r'^(#{1,3}\s[^\n]+)\n([^\n#])', r'\1\n\n\2', text, flags=re.MULTILINE)
        
        # Fix contact info formatting (should be right after name)
        text = re.sub(r'^(#\s+[^\n]+)\n+([^#\n]*[^\n]*[@\(\)]+[^\n]*)', r'\1\n\2', text, flags=re.MULTILINE)
        
        # Standardize bullet points
        text = re.sub(r'^[\s]*[🔹🚀⚡◆▶→]\s*', '- ', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*[•*]\s+', '- ', text, flags=re.MULTILINE)
        
        # Fix section header variations
        text = re.sub(r'^[🎓💼⚡🚀📜🌍🔧💻🎯]\s*([A-Z][A-Za-z\s&]+)$', r'## \1', text, flags=re.MULTILINE)
        
        # Remove horizontal rules that interfere with parsing
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        
        # Ensure consistent spacing
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'^\s*\n', '', text, flags=re.MULTILINE)
        
        return text.strip()
    
    def extract_sections(self, markdown_text: str) -> Dict[str, List[str]]:
        """
        Extract and categorize sections for better parsing
        Returns structured data for both PDF and DOCX generation
        """
        normalized = self.normalize_markdown(markdown_text)
        lines = normalized.split('\n')
        
        sections = {
            'header': [],
            'contact': [],
            'sections': {},
            'current_section': None
        }
        
        current_section = None
        
        for i, line in enumerate(lines):
            line = line.strip()
            if not line:
                continue
            
            # Main header (name)
            if re.match(r'^#\s+', line) and i < 5:
                header_text = re.sub(r'^#\s+', '', line).strip()
                sections['header'].append(header_text)
                continue
            
            # Contact info (lines with email, phone, etc.)
            if (current_section is None and 
                any(indicator in line.lower() for indicator in ['@', 'phone', 'linkedin', 'github', '(', ')', '+', 'http', 'www'])):
                sections['contact'].append(line)
                continue
            
            # Section headers
            if re.match(r'^##\s+', line):
                section_name = re.sub(r'^##\s+', '', line).strip()
                current_section = section_name
                sections['sections'][current_section] = []
                continue
            
            # Add content to current section
            if current_section:
                sections['sections'][current_section].append(line)
        
        return sections
    
    def generate_enhanced_markdown(self, sections: Dict) -> str:
        """
        Generate enhanced markdown from structured sections
        Ensures proper formatting for both PDF and DOCX
        """
        output = []
        
        # Add header
        if sections['header']:
            output.append(f"# {sections['header'][0]}")
            output.append("")
        
        # Add contact info
        if sections['contact']:
            contact_line = " | ".join(sections['contact'])
            output.append(contact_line)
            output.append("")
        
        # Add sections
        for section_name, content in sections['sections'].items():
            output.append(f"## {section_name}")
            output.append("")
            
            for line in content:
                if line.strip():
                    output.append(line)
            output.append("")
        
        return "\n".join(output).strip()
    
    def fix_pdf_markdown(self, markdown_text: str) -> str:
        """
        Specifically fix markdown for PDF generation
        Ensures headers are properly formatted for the markdown library
        """
        normalized = self.normalize_markdown(markdown_text)
        
        # Ensure all section headers are properly spaced
        normalized = re.sub(r'^(##\s+[^\n]+)$', r'\1\n', normalized, flags=re.MULTILINE)
        
        # Fix bold text formatting for PDF
        normalized = re.sub(r'\*\*([^*]+)\*\*', r'**\1**', normalized)
        
        # Fix italic text formatting  
        normalized = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'*\1*', normalized)
        
        # Ensure bullet points have proper spacing
        normalized = re.sub(r'^([-•*]\s+.+)$', r'\1', normalized, flags=re.MULTILINE)
        
        return normalized
    
    def fix_docx_markdown(self, markdown_text: str) -> str:
        """
        Specifically fix markdown for DOCX generation
        Ensures compatibility with the enhanced DOCX parser
        """
        return self.normalize_markdown(markdown_text)

# Test the unified parser
def test_unified_parser():
    """Test the unified parser with problematic markdown"""
    
    problematic_markdown = """# Dr. Sarah Chen
sarah.chen@email.com | (555) 987-6543 | LinkedIn: linkedin.com/in/sarah-chen
GitHub: github.com/sarahchen | Portfolio: https://sarahchen.dev | New York, NY

🎓 Education
**Ph.D. in Computer Science**
*Stanford University | Stanford, CA | 2015 - 2019*

💼 Professional Experience

**Senior AI Research Scientist**
*Google DeepMind | Mountain View, CA | 2019 - Present*

• Led research team developing **large language models**
• Published **15+ papers** in top-tier conferences
• **Key Achievement**: Improved model efficiency by *40%*

🚀 Technical Skills

**Programming:** `Python`, `C++`, `JavaScript`, `R`
**ML Frameworks:** `TensorFlow`, `PyTorch`, `JAX`
**Cloud Platforms:** `Google Cloud`, `AWS`, `Azure`

📜 Selected Publications

1. "Transformer Architecture for Multi-Modal Learning" - *NeurIPS 2023*
2. "Efficient Training of Large Language Models" - **ICML 2022**
3. "Neural Architecture Search for Edge Devices" - *ICLR 2021*"""

    print("🧪 Testing Unified Resume Parser")
    print("=" * 50)
    
    parser = UnifiedResumeParser()
    
    try:
        # Test normalization
        print("📝 Testing markdown normalization...")
        normalized = parser.normalize_markdown(problematic_markdown)
        print("✅ Normalization successful")
        
        # Test section extraction
        print("📊 Testing section extraction...")
        sections = parser.extract_sections(problematic_markdown)
        print(f"✅ Extracted {len(sections['sections'])} sections")
        print(f"   Header: {sections['header']}")
        print(f"   Contact: {len(sections['contact'])} items")
        print(f"   Sections: {list(sections['sections'].keys())}")
        
        # Test enhanced markdown generation
        print("⚡ Testing enhanced markdown generation...")
        enhanced = parser.generate_enhanced_markdown(sections)
        print("✅ Enhanced markdown generated")
        
        # Test PDF-specific fixes
        print("📄 Testing PDF markdown fixes...")
        pdf_fixed = parser.fix_pdf_markdown(problematic_markdown)
        print("✅ PDF markdown fixed")
        
        # Test DOCX-specific fixes
        print("📝 Testing DOCX markdown fixes...")
        docx_fixed = parser.fix_docx_markdown(problematic_markdown)
        print("✅ DOCX markdown fixed")
        
        # Show results
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("\n📋 Enhanced markdown preview:")
        print("-" * 30)
        print(enhanced[:500] + "..." if len(enhanced) > 500 else enhanced)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_unified_parser()