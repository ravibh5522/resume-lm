#!/usr/bin/env python3
"""
Advanced PDF Generator V2 - Optimized for A4 layout with proper formatting
"""

import re
import base64
from io import BytesIO
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import markdown
from markdown.extensions import tables, codehilite
from typing import Optional

class AdvancedPDFGeneratorV2:
    def __init__(self):
        self.font_config = FontConfiguration()
        
    def get_optimized_css(self) -> str:
        """Get optimized CSS for A4 resume layout"""
        return """
        @page {
            size: A4;
            margin: 0.5in 0.6in;  /* Reduced margins for more content */
            @bottom-center {
                content: counter(page) " of " counter(pages);
                font-size: 10px;
                color: #666;
            }
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            font-size: 11px;  /* Slightly smaller for more content */
            line-height: 1.4;  /* Tighter line height */
            color: #333;
            background: white;
        }
        
        /* Header Section */
        h1 {
            font-size: 24px;
            font-weight: bold;
            color: #1e3a8a;  /* Navy blue */
            text-align: center;
            margin-bottom: 4px;
            letter-spacing: 1px;
        }
        
        .contact-info {
            text-align: center;
            margin-bottom: 12px;
            font-size: 10px;
            color: #666;
        }
        
        .contact-info a {
            color: #0891b2;  /* Teal */
            text-decoration: none;
        }
        
        /* Section Headers */
        h2 {
            font-size: 14px;
            font-weight: bold;
            color: #1e3a8a;
            margin-top: 12px;
            margin-bottom: 6px;
            padding-bottom: 2px;
            border-bottom: 2px solid #0891b2;
            display: flex;
            align-items: center;
        }
        
        h2::before {
            margin-right: 6px;
            font-size: 16px;
        }
        
        h3 {
            font-size: 12px;
            font-weight: bold;
            color: #1e3a8a;
            margin-top: 8px;
            margin-bottom: 3px;
        }
        
        /* Compact spacing for content */
        p {
            margin-bottom: 4px;
            text-align: justify;
        }
        
        /* Experience and Education entries */
        .job-title {
            font-weight: bold;
            color: #1e3a8a;
            font-size: 12px;
        }
        
        .company-info {
            color: #666;
            font-size: 10px;
            font-style: italic;
            margin-bottom: 3px;
        }
        
        /* Lists */
        ul {
            margin: 4px 0 8px 0;
            padding-left: 16px;
        }
        
        li {
            margin-bottom: 2px;
            line-height: 1.3;
        }
        
        /* Skills section - compact grid */
        .skills-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 8px;
            margin: 6px 0;
        }
        
        .skill-category {
            margin-bottom: 6px;
        }
        
        .skill-category strong {
            color: #1e3a8a;
            font-size: 11px;
        }
        
        /* Projects - compact layout */
        .project {
            margin-bottom: 8px;
            page-break-inside: avoid;
        }
        
        .project-title {
            font-weight: bold;
            color: #1e3a8a;
            font-size: 11px;
        }
        
        .project-tech {
            font-size: 10px;
            color: #666;
            font-style: italic;
            margin-bottom: 2px;
        }
        
        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 6px 0;
            font-size: 10px;
        }
        
        th, td {
            padding: 3px 6px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        
        th {
            background-color: #f8fafc;
            font-weight: bold;
            color: #1e3a8a;
        }
        
        /* Links */
        a {
            color: #0891b2;
            text-decoration: none;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            height: 1px;
            background: linear-gradient(to right, #1e3a8a, #0891b2, #1e3a8a);
            margin: 8px 0;
        }
        
        /* Emoji replacements for better PDF rendering */
        .emoji {
            font-weight: bold;
            color: #0891b2;
        }
        
        /* Code and technical elements */
        code {
            background-color: #f1f5f9;
            padding: 1px 3px;
            border-radius: 2px;
            font-family: 'Courier New', monospace;
            font-size: 10px;
        }
        
        /* Page break control */
        .page-break-avoid {
            page-break-inside: avoid;
        }
        
        .no-break {
            page-break-inside: avoid;
        }
        
        /* First page optimization */
        .first-page {
            page-break-before: avoid;
        }
        
        /* Compact spacing for better fit */
        .compact {
            margin: 2px 0;
        }
        
        /* Professional summary - highlighted */
        .summary {
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 8px;
            border-left: 4px solid #0891b2;
            margin: 8px 0;
            border-radius: 4px;
        }
        
        /* Certifications and achievements */
        .achievement {
            margin: 2px 0;
            padding-left: 12px;
            position: relative;
        }
        
        .achievement::before {
            content: "🏅";
            position: absolute;
            left: 0;
            color: #0891b2;
        }
        """
    
    def preprocess_markdown(self, markdown_text: str) -> str:
        """Preprocess markdown for better PDF rendering"""
        
        # Replace emoji with CSS classes for better rendering
        emoji_replacements = {
            '🚀': '<span class="emoji">★</span>',
            '💼': '<span class="emoji">●</span>',
            '🎓': '<span class="emoji">◆</span>',
            '⚡': '<span class="emoji">▸</span>',
            '🔹': '<span class="emoji">•</span>',
            '◆': '<span class="emoji">▸</span>',
            '🏅': '<span class="emoji">★</span>',
            '🌍': '<span class="emoji">◯</span>',
            '📜': '<span class="emoji">■</span>',
            '⭐': '<span class="emoji">★</span>',
        }
        
        processed_text = markdown_text
        for emoji, replacement in emoji_replacements.items():
            processed_text = processed_text.replace(emoji, replacement)
        
        # Add CSS classes for better structure
        lines = processed_text.split('\n')
        processed_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Add compact class to list items
            if stripped.startswith('◆') or stripped.startswith('•') or stripped.startswith('▸'):
                line = f'<div class="compact">{line}</div>'
            
            # Add no-break class to job titles and important sections
            elif stripped and not stripped.startswith('#') and ':' in stripped and len(stripped) < 100:
                line = f'<div class="no-break">{line}</div>'
            
            processed_lines.append(line)
        
        return '\n'.join(processed_lines)
    
    def markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML with proper formatting"""
        
        # Preprocess the markdown
        processed_markdown = self.preprocess_markdown(markdown_text)
        
        # Configure markdown with extensions
        md = markdown.Markdown(
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.tables',
                'markdown.extensions.nl2br',
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': False,
                }
            }
        )
        
        # Convert to HTML
        html_content = md.convert(processed_markdown)
        
        # Post-process HTML for better PDF rendering
        html_content = self.post_process_html(html_content)
        
        return html_content
    
    def post_process_html(self, html_content: str) -> str:
        """Post-process HTML for better PDF layout"""
        
        # Wrap the first section (name and contact) in a special div
        html_content = re.sub(
            r'(<h1>.*?</h1>\s*<p>.*?</p>)',
            r'<div class="first-page">\1</div>',
            html_content,
            flags=re.DOTALL
        )
        
        # Add page-break-avoid to experience entries
        html_content = re.sub(
            r'(<h3>.*?</h3>.*?(?=<h3>|<h2>|$))',
            r'<div class="page-break-avoid">\1</div>',
            html_content,
            flags=re.DOTALL
        )
        
        # Wrap professional summary
        html_content = re.sub(
            r'(<h2[^>]*>.*?PROFESSIONAL SUMMARY.*?</h2>\s*<p>.*?</p>)',
            r'<div class="summary">\1</div>',
            html_content,
            flags=re.DOTALL | re.IGNORECASE
        )
        
        return html_content
    
    def generate_pdf_from_markdown(self, markdown_content: str) -> bytes:
        """Generate PDF from markdown content with optimized layout"""
        
        # Convert markdown to HTML
        html_content = self.markdown_to_html(markdown_content)
        
        # Create complete HTML document
        full_html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Professional Resume</title>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Get CSS
        css_content = self.get_optimized_css()
        
        try:
            # Generate PDF with WeasyPrint
            html_doc = HTML(string=full_html)
            css_doc = CSS(string=css_content, font_config=self.font_config)
            
            pdf_bytes = html_doc.write_pdf(
                stylesheets=[css_doc],
                font_config=self.font_config,
                optimize_images=True,
                presentational_hints=True
            )
            
            if pdf_bytes is None:
                raise ValueError("PDF generation returned None")
            
            return pdf_bytes
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            raise
    
    def generate_pdf_base64(self, markdown_content: str) -> str:
        """Generate PDF and return as base64 string"""
        pdf_bytes = self.generate_pdf_from_markdown(markdown_content)
        return base64.b64encode(pdf_bytes).decode('utf-8')

def test_pdf_generator():
    """Test the PDF generator"""
    sample_markdown = """
# John Doe

San Francisco, CA | (555) 123-4567 | john.doe@email.com
[LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)

---

## 🚀 PROFESSIONAL SUMMARY

Experienced Software Engineer with 5+ years developing scalable web applications.

## 💼 PROFESSIONAL EXPERIENCE

### Senior Software Engineer
**Tech Corp** | San Francisco, CA | 2022 - Present

◆ Led development of microservices architecture
◆ Improved system performance by 40%
◆ Mentored junior developers

### Software Developer
**StartupXYZ** | San Francisco, CA | 2020 - 2022

◆ Built REST APIs using Python and Django
◆ Collaborated with cross-functional teams

## 🎓 EDUCATION

### Bachelor of Science in Computer Science
**UC Berkeley** | Berkeley, CA | 2016 - 2020
"""
    
    generator = AdvancedPDFGeneratorV2()
    pdf_base64 = generator.generate_pdf_base64(sample_markdown)
    print(f"✅ PDF generated successfully! Length: {len(pdf_base64)} characters")
    return True

if __name__ == "__main__":
    test_pdf_generator()