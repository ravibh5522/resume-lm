#!/usr/bin/env python3
"""
Enhanced PDF Generator with Fixed Header Parsing
Uses unified parser to ensure ## headers work properly
"""

import base64
import io
import re
import markdown
from weasyprint import HTML, CSS
from unified_parser import UnifiedResumeParser

class EnhancedPdfGenerator:
    """
    Enhanced PDF generator that properly handles ## headers and formatting
    Uses unified parser for consistent results
    """
    
    def __init__(self):
        self.parser = UnifiedResumeParser()
        self.css_styles = """
        @page {
            margin: 0.75in;
            size: A4;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.6;
            color: #2c3e50;
            font-size: 11pt;
            max-width: 100%;
        }
        
        /* HEADER STYLES - CRITICAL FOR ## PARSING */
        h1 {
            font-size: 24pt;
            font-weight: bold;
            color: #1a365d;
            text-align: center;
            margin-bottom: 8pt;
            margin-top: 0;
            border-bottom: 2px solid #3182ce;
            padding-bottom: 8pt;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            color: #2b6cb0;
            margin-top: 20pt;
            margin-bottom: 10pt;
            border-bottom: 1px solid #cbd5e0;
            padding-bottom: 4pt;
            text-transform: uppercase;
            letter-spacing: 0.5pt;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #2d3748;
            margin-top: 15pt;
            margin-bottom: 8pt;
        }
        
        /* Contact info styling */
        .contact-info {
            text-align: center;
            font-size: 10pt;
            color: #4a5568;
            margin-bottom: 20pt;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 10pt;
        }
        
        /* Professional formatting */
        p {
            margin-bottom: 8pt;
            text-align: justify;
        }
        
        strong {
            color: #2d3748;
            font-weight: bold;
        }
        
        em {
            color: #4a5568;
            font-style: italic;
        }
        
        code {
            background-color: #f7fafc;
            color: #e53e3e;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10pt;
        }
        
        /* List styling */
        ul {
            margin: 10pt 0;
            padding-left: 20pt;
        }
        
        li {
            margin-bottom: 6pt;
            line-height: 1.5;
        }
        
        ol {
            margin: 10pt 0;
            padding-left: 20pt;
        }
        
        /* Job entries */
        .job-entry {
            margin-bottom: 15pt;
        }
        
        .job-title {
            font-weight: bold;
            color: #2d3748;
        }
        
        .company-info {
            font-style: italic;
            color: #4a5568;
            margin-bottom: 5pt;
        }
        
        /* Skills and technical info */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200pt, 1fr));
            gap: 10pt;
            margin: 10pt 0;
        }
        
        /* Links */
        a {
            color: #3182ce;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Ensure proper spacing */
        .section {
            margin-bottom: 20pt;
        }
        
        /* Fix table formatting if present */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10pt 0;
        }
        
        th, td {
            padding: 6pt;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
        }
        
        th {
            font-weight: bold;
            color: #2b6cb0;
        }
        """
    
    def preprocess_markdown_enhanced(self, markdown_text: str) -> str:
        """
        Enhanced preprocessing that ensures ## headers are parsed correctly
        """
        # Use unified parser for consistent formatting
        fixed_text = self.parser.fix_pdf_markdown(markdown_text)
        
        # Additional PDF-specific preprocessing
        lines = fixed_text.split('\n')
        processed_lines = []
        
        for line in lines:
            line = line.strip()
            
            # Skip empty lines but preserve spacing
            if not line:
                processed_lines.append('')
                continue
            
            # Ensure section headers are properly formatted
            if re.match(r'^##\s+', line):
                section_title = re.sub(r'^##\s+', '', line).strip()
                processed_lines.append(f"## {section_title}")
                continue
            
            # Handle contact info line (detect by common patterns)
            if (not any(processed_lines) or 
                (len(processed_lines) < 5 and 
                 any(indicator in line.lower() for indicator in ['@', 'phone', 'linkedin', 'github', '(', ')', '+', 'http']))):
                # Format as contact info
                processed_lines.append(f'<div class="contact-info">{line}</div>')
                continue
            
            # Handle job titles and company info
            if re.match(r'^\*\*[^*]+\*\*\s*$', line):
                # Job title
                processed_lines.append(f'<div class="job-entry">')
                processed_lines.append(f'<div class="job-title">{line}</div>')
                continue
            
            if re.match(r'^\*[^*]+\*\s*$', line) and processed_lines and 'job-title' in processed_lines[-1]:
                # Company info following job title
                processed_lines.append(f'<div class="company-info">{line}</div>')
                processed_lines.append('</div>')
                continue
            
            # Regular content
            processed_lines.append(line)
        
        result = '\n'.join(processed_lines)
        
        # Debug print to see what we're sending to markdown processor
        print(f"📋 Enhanced preprocessing result preview:")
        print(f"   First 300 chars: {result[:300]}...")
        print(f"   Contains ## headers: {bool(re.search(r'^##\s+', result, re.MULTILINE))}")
        
        return result
    
    def markdown_to_html_enhanced(self, markdown_text: str) -> str:
        """
        Convert markdown to HTML with enhanced header support
        """
        # Preprocess the markdown
        processed_markdown = self.preprocess_markdown_enhanced(markdown_text)
        
        # Configure markdown processor with extensions for better header handling
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.nl2br',
            'markdown.extensions.sane_lists',
            'markdown.extensions.toc',
        ])
        
        # Convert to HTML
        html_content = md.convert(processed_markdown)
        
        # Post-process HTML to ensure headers are properly formatted
        html_content = re.sub(r'<h2>([^<]+)</h2>', r'<h2 class="section-header">\1</h2>', html_content)
        html_content = re.sub(r'<h1>([^<]+)</h1>', r'<h1 class="main-header">\1</h1>', html_content)
        
        # Debug the HTML output
        h2_matches = re.findall(r'<h2[^>]*>([^<]+)</h2>', html_content)
        print(f"🔍 HTML conversion debug:")
        print(f"   Found {len(h2_matches)} h2 headers: {h2_matches}")
        print(f"   HTML preview: {html_content[:500]}...")
        
        return html_content
    
    def generate_pdf_base64_enhanced(self, markdown_text: str) -> str:
        """
        Generate PDF from markdown with enhanced header parsing
        Returns base64 encoded PDF
        """
        try:
            print("🚀 Starting enhanced PDF generation...")
            
            # Convert markdown to HTML using enhanced processor
            html_content = self.markdown_to_html_enhanced(markdown_text)
            
            # Create complete HTML document
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Resume</title>
                <style>{self.css_styles}</style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Generate PDF
            print("📄 Converting HTML to PDF...")
            pdf_buffer = io.BytesIO()
            html_doc = HTML(string=full_html)
            html_doc.write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            
            # Encode to base64
            pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
            print(f"✅ Enhanced PDF generated successfully! Size: {len(pdf_base64)} characters")
            
            return pdf_base64
            
        except Exception as e:
            print(f"❌ Enhanced PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            raise

# Alternative: PDF to markdown to DOCX converter
def pdf_to_docx_converter(pdf_content: bytes) -> str:
    """
    Convert PDF content to DOCX via markdown extraction
    This is for cases where direct PDF parsing is preferred
    """
    try:
        # This would require additional libraries like PyMuPDF or pdfplumber
        # For now, return a placeholder
        print("⚠️  PDF to DOCX conversion would require PyMuPDF or pdfplumber")
        print("   Consider using the enhanced generators instead")
        return ""
    except Exception as e:
        print(f"❌ PDF to DOCX conversion failed: {e}")
        return ""

# Test the enhanced PDF generator
def test_enhanced_pdf_generator():
    """Test the enhanced PDF generator with problematic markdown"""
    
    test_markdown = """# Dr. Sarah Chen
sarah.chen@email.com | (555) 987-6543 | LinkedIn: linkedin.com/in/sarah-chen

## Education

**Ph.D. in Computer Science**
*Stanford University | 2015 - 2019*

## Professional Experience  

**Senior AI Research Scientist**
*Google DeepMind | 2019 - Present*

- Led research team developing **large language models**
- Published **15+ papers** in top-tier conferences
- **Key Achievement**: Improved model efficiency by *40%*

## Technical Skills

**Programming:** `Python`, `C++`, `JavaScript`
**ML Frameworks:** `TensorFlow`, `PyTorch`, `JAX`

## Selected Publications

1. "Transformer Architecture for Multi-Modal Learning" - *NeurIPS 2023*
2. "Efficient Training of Large Language Models" - **ICML 2022**"""

    print("🧪 Testing Enhanced PDF Generator")
    print("=" * 50)
    
    try:
        generator = EnhancedPdfGenerator()
        
        # Test preprocessing
        print("📝 Testing enhanced preprocessing...")
        preprocessed = generator.preprocess_markdown_enhanced(test_markdown)
        print("✅ Preprocessing successful")
        
        # Test HTML conversion
        print("🌐 Testing HTML conversion...")
        html = generator.markdown_to_html_enhanced(test_markdown)
        print("✅ HTML conversion successful")
        
        # Test PDF generation
        print("📄 Testing PDF generation...")
        pdf_base64 = generator.generate_pdf_base64_enhanced(test_markdown)
        print(f"✅ PDF generation successful! Size: {len(pdf_base64)} chars")
        
        print("\n" + "=" * 50)
        print("🎉 ALL ENHANCED PDF TESTS PASSED!")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_enhanced_pdf_generator()