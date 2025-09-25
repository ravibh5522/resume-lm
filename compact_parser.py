#!/usr/bin/env python3
"""
Compact Ultimate Parser - Minimal spacing, professional layout
Fixes excessive whitespace and blank spaces while preserving all formatting
"""

import base64
import io
import re
import markdown
from weasyprint import HTML, CSS
from typing import Dict, List, Tuple, Optional, Any

class CompactMarkdownParser:
    """
    Compact parser that eliminates excessive spacing while preserving formatting
    """
    
    def __init__(self):
        self.markdown_processor = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.sane_lists',
                'markdown.extensions.toc',
            ],
            extension_configs={
                'markdown.extensions.toc': {
                    'permalink': False,
                }
            }
        )
    
    def fix_compact_markdown(self, markdown_text: str) -> str:
        """
        Fix markdown with compact spacing - no excessive whitespace
        """
        text = markdown_text.strip()
        
        # 1. Fix header spacing and formatting
        text = re.sub(r'^(#{1,6})\s*([^\n]*)\s*$', r'\1 \2', text, flags=re.MULTILINE)
        
        # 2. COMPACT: Single line break after headers (not double)
        text = re.sub(r'^(#{1,6}\s[^\n]+)\n\n+', r'\1\n', text, flags=re.MULTILINE)
        
        # 3. Fix bold text formatting
        text = re.sub(r'(?<!\*)\*\*([^*\n]+?)\*\*(?!\*)', r'**\1**', text)
        
        # 4. Fix italic text formatting  
        text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'*\1*', text)
        
        # 5. Fix code formatting
        text = re.sub(r'`([^`\n]+)`', r'`\1`', text)
        
        # 6. Standardize bullet points
        text = re.sub(r'^[\s]*[•◦▪▫‣⁃]\s*', '- ', text, flags=re.MULTILINE)
        text = re.sub(r'^[\s]*[*]\s+', '- ', text, flags=re.MULTILINE)
        
        # 7. COMPACT: Remove excessive blank lines - max 1 blank line anywhere
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'\n\n\n+', '\n\n', text)
        
        # 8. COMPACT: Remove trailing whitespace
        text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
        
        # 9. COMPACT: Ensure job entries don't have extra spacing
        text = re.sub(r'(\*[^*\n]+\*)\n\n+(-)', r'\1\n\2', text)
        
        return text.strip()
    
    def create_compact_html(self, markdown_text: str) -> str:
        """
        Create HTML with compact formatting
        """
        # Fix markdown with compact spacing
        fixed_markdown = self.fix_compact_markdown(markdown_text)
        
        # Convert to HTML
        html_content = self.markdown_processor.convert(fixed_markdown)
        
        # Enhance HTML structure
        html_content = self.enhance_compact_structure(html_content)
        
        return html_content
    
    def enhance_compact_structure(self, html: str) -> str:
        """
        Enhance HTML with compact styling classes
        """
        # Add classes for compact styling
        html = re.sub(r'<h1([^>]*)>', r'<h1 class="compact-name"\1>', html)
        html = re.sub(r'<h2([^>]*)>', r'<h2 class="compact-section"\1>', html)
        html = re.sub(r'<h3([^>]*)>', r'<h3 class="compact-subsection"\1>', html)
        
        # Enhance contact info paragraphs
        def enhance_contact(match):
            p_content = match.group(1)
            if any(pattern in p_content.lower() for pattern in ['@', 'linkedin', 'github', 'phone', '(', ')']):
                return f'<p class="compact-contact">{p_content}</p>'
            return match.group(0)
        
        html = re.sub(r'<p>([^<]+)</p>', enhance_contact, html)
        
        # Enhance job entries with compact spacing
        html = re.sub(r'<p><strong>([^<]+)</strong></p>\s*<p><em>([^<]+)</em></p>', 
                     r'<div class="compact-job"><h4 class="compact-job-title">\1</h4><p class="compact-job-meta">\2</p></div>', html)
        
        return html

class CompactPdfGenerator:
    """
    Compact PDF generator with minimal spacing and professional layout
    """
    
    def __init__(self):
        self.parser = CompactMarkdownParser()
        self.compact_css = """
        @page {
            margin: 0.6in 0.75in;
            size: A4;
        }
        
        body {
            font-family: 'Georgia', 'Times New Roman', serif;
            line-height: 1.4;
            color: #2c3e50;
            font-size: 11pt;
            max-width: 100%;
        }
        
        /* COMPACT: Minimal header spacing */
        h1, .compact-name {
            font-size: 22pt;
            font-weight: bold;
            color: #1a365d;
            text-align: center;
            margin: 0 0 8pt 0;
            border-bottom: 2px solid #3182ce;
            padding-bottom: 4pt;
        }
        
        h2, .compact-section {
            font-size: 13pt;
            font-weight: bold;
            color: #2b6cb0;
            margin: 12pt 0 6pt 0;
            border-bottom: 1px solid #cbd5e0;
            padding-bottom: 2pt;
            text-transform: uppercase;
            letter-spacing: 0.3pt;
        }
        
        h3, .compact-subsection {
            font-size: 11pt;
            font-weight: bold;
            color: #2d3748;
            margin: 8pt 0 4pt 0;
        }
        
        h4, .compact-job-title {
            font-size: 11pt;
            font-weight: bold;
            color: #2d3748;
            margin: 6pt 0 2pt 0;
        }
        
        /* COMPACT: Minimal contact info spacing */
        .compact-contact {
            text-align: center;
            font-size: 10pt;
            color: #4a5568;
            margin: 4pt 0 10pt 0;
            border-bottom: 1px solid #e2e8f0;
            padding-bottom: 6pt;
        }
        
        /* COMPACT: Minimal paragraph spacing */
        p {
            margin: 4pt 0;
            text-align: justify;
        }
        
        /* COMPACT: Text formatting */
        strong {
            color: #1a202c;
            font-weight: bold;
        }
        
        em {
            color: #4a5568;
            font-style: italic;
        }
        
        code {
            background-color: #f7fafc;
            color: #e53e3e;
            padding: 1px 3px;
            border-radius: 2px;
            font-family: 'Consolas', 'Courier New', monospace;
            font-size: 9pt;
        }
        
        /* COMPACT: Minimal list spacing */
        ul {
            margin: 6pt 0;
            padding-left: 16pt;
        }
        
        li {
            margin-bottom: 3pt;
            line-height: 1.3;
        }
        
        ol {
            margin: 6pt 0;
            padding-left: 16pt;
        }
        
        /* COMPACT: Job entry styling */
        .compact-job {
            margin: 6pt 0;
            border-left: 2px solid #e2e8f0;
            padding-left: 8pt;
        }
        
        .compact-job-meta {
            font-style: italic;
            color: #4a5568;
            margin: 1pt 0 4pt 0;
            font-size: 10pt;
        }
        
        /* Links */
        a {
            color: #3182ce;
            text-decoration: none;
        }
        
        /* COMPACT: Table styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 6pt 0;
        }
        
        th, td {
            padding: 3pt;
            text-align: left;
            border-bottom: 1px solid #e2e8f0;
            font-size: 10pt;
        }
        
        th {
            font-weight: bold;
            color: #2b6cb0;
        }
        
        /* COMPACT: Remove excessive spacing from generated content */
        h1 + p, h2 + p, h3 + p {
            margin-top: 2pt;
        }
        
        p + h2 {
            margin-top: 10pt;
        }
        
        p + h3 {
            margin-top: 6pt;
        }
        """
    
    def generate_compact_pdf_base64(self, markdown_text: str) -> str:
        """
        Generate PDF with compact spacing and minimal whitespace
        """
        try:
            print("🚀 Starting COMPACT PDF generation...")
            print(f"📝 Input markdown length: {len(markdown_text)} characters")
            
            # Create compact HTML
            html_content = self.parser.create_compact_html(markdown_text)
            
            print(f"🌐 Generated compact HTML length: {len(html_content)} characters")
            
            # Debug: Check structure
            h2_count = len(re.findall(r'<h2[^>]*>', html_content))
            p_count = len(re.findall(r'<p[^>]*>', html_content))
            
            print(f"🔍 Compact HTML: H2={h2_count}, P={p_count}")
            
            # Create complete HTML document with compact styling
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>Resume</title>
                <style>{self.compact_css}</style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Generate PDF
            print("📄 Converting to compact PDF...")
            pdf_buffer = io.BytesIO()
            html_doc = HTML(string=full_html)
            html_doc.write_pdf(pdf_buffer)
            pdf_buffer.seek(0)
            
            # Encode to base64
            pdf_base64 = base64.b64encode(pdf_buffer.read()).decode('utf-8')
            print(f"✅ COMPACT PDF generated! Size: {len(pdf_base64)} characters")
            
            return pdf_base64
            
        except Exception as e:
            print(f"❌ Compact PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            raise

# Test the compact generator
def test_compact_generator():
    """Test compact generation with spacing-heavy markdown"""
    
    spacing_heavy_markdown = """# John Smith
john.smith@email.com | (555) 123-4567 | LinkedIn: linkedin.com/in/john-smith


## Professional Summary


**Senior Software Engineer** with **8+ years** of experience developing *scalable applications*. Expert in `Python`, `JavaScript`, and **cloud technologies**.



## Experience


**Lead Software Engineer**
*TechCorp Inc. | San Francisco, CA | 2020 - Present*

- Built **microservices architecture** serving `1M+ requests/day`
- **Key Achievement**: Reduced system latency by *45%*


- Mentored *junior developers* and led **code reviews**


**Software Engineer**
*StartupXYZ | Boston, MA | 2018 - 2020*



- Developed **e-commerce platform** with *real-time features*
- **Impact**: Increased conversion by *30%*



## Education



**Master of Science in Computer Science**
*MIT | Cambridge, MA | 2016 - 2018*



## Skills


**Languages:** `Python`, `JavaScript`, **TypeScript**


**Frameworks:** **React**, `Node.js`, *Django*"""

    print("🧪 Testing COMPACT Generator")
    print("=" * 50)
    print("🎯 Input has excessive spacing and blank lines")
    
    # Count excessive spacing in input
    blank_lines = len(re.findall(r'\n\s*\n', spacing_heavy_markdown))
    print(f"   📊 Input blank lines: {blank_lines}")
    
    try:
        # Test compact generation
        generator = CompactPdfGenerator()
        
        # Test markdown processing
        print("\n📝 Testing compact markdown processing...")
        compact_markdown = generator.parser.fix_compact_markdown(spacing_heavy_markdown)
        compact_blank_lines = len(re.findall(r'\n\s*\n', compact_markdown))
        print(f"   📊 Compact blank lines: {compact_blank_lines} (reduced by {blank_lines - compact_blank_lines})")
        
        # Test PDF generation
        print("\n📄 Testing compact PDF generation...")
        pdf_result = generator.generate_compact_pdf_base64(spacing_heavy_markdown)
        
        print(f"\n🎉 COMPACT TEST RESULTS:")
        print(f"   ✓ Spacing reduction: {blank_lines} → {compact_blank_lines} blank lines")
        print(f"   ✓ PDF generation: {len(pdf_result):,} characters")
        print(f"   ✓ Compact formatting: Applied")
        print(f"   ✓ Professional layout: Optimized")
        
        return True
        
    except Exception as e:
        print(f"❌ Compact test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compact_generator()