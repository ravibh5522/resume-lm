#!/usr/bin/env python3
"""
Optimized PDF Generator for Resume - Single Page A4 Layout
"""

import markdown
import weasyprint
import base64
from typing import Optional
import re

class OptimizedPDFGenerator:
    def __init__(self):
        self.css_styles = """
        @page {
            size: A4;
            margin: 0.5in;
            @top-center {
                content: "";
            }
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11px;
            line-height: 1.3;
            color: #333;
            margin: 0;
            padding: 0;
        }
        
        /* Header */
        h1 {
            color: #2c5aa0;
            font-size: 24px;
            text-align: center;
            margin: 0 0 8px 0;
            font-weight: bold;
        }
        
        /* Contact info under name - single line format */
        h1 + p {
            text-align: center;
            font-size: 10px;
            color: #666;
            margin: 0 0 15px 0;
            line-height: 1.4;
        }
        
        /* Section headers */
        h2 {
            color: #2c5aa0;
            font-size: 14px;
            margin: 12px 0 6px 0;
            padding-bottom: 2px;
            border-bottom: 2px solid #17a2b8;
            font-weight: bold;
        }
        
        h3 {
            color: #333;
            font-size: 12px;
            margin: 8px 0 4px 0;
            font-weight: bold;
        }
        
        /* Paragraphs */
        p {
            margin: 4px 0;
            text-align: justify;
        }
        
        /* Lists */
        ul {
            margin: 4px 0;
            padding-left: 16px;
        }
        
        li {
            margin: 2px 0;
            line-height: 1.2;
        }
        
        /* Remove extra spacing */
        * {
            page-break-inside: avoid;
        }
        
        /* Compact spacing for sections */
        .section {
            margin-bottom: 10px;
        }
        
        /* Tables for structured data */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 4px 0;
            font-size: 10px;
        }
        
        td {
            padding: 2px 4px;
            vertical-align: top;
        }
        
        /* Strong text */
        strong {
            color: #2c5aa0;
            font-weight: bold;
        }
        
        /* Links */
        a {
            color: #17a2b8;
            text-decoration: none;
        }
        
        /* Emojis smaller */
        .emoji {
            font-size: 10px;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            border-top: 1px solid #ddd;
            margin: 8px 0;
        }
        
        /* Code/tech skills */
        code {
            background-color: #f8f9fa;
            padding: 1px 3px;
            border-radius: 2px;
            font-size: 10px;
        }
        
        /* Compact job entries */
        .job-entry {
            margin-bottom: 8px;
        }
        
        .job-title {
            font-weight: bold;
            color: #2c5aa0;
        }
        
        .job-company {
            color: #666;
            font-style: italic;
        }
        
        .job-date {
            color: #888;
            font-size: 10px;
        }
        """
    
    def preprocess_markdown(self, markdown_text: str) -> str:
        """Clean and optimize markdown for better PDF rendering"""
        
        # Remove excessive line breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', markdown_text)
        
        # Fix header formatting - ensure contact info is right after name
        text = re.sub(r'^(#\s+[^\n]+)\n+([^\n]*@[^\n]*)', r'\1\n\n\2', text, flags=re.MULTILINE)
        
        # Convert emoji bullets to simple bullets
        text = re.sub(r'^[\s]*[🔹🚀⚡◆▶]\s*', '• ', text, flags=re.MULTILINE)
        
        # Fix section headers
        text = re.sub(r'^---+$', '', text, flags=re.MULTILINE)
        text = re.sub(r'^[🎓💼⚡🚀📜🌍]\s*([A-Z][^#\n]+)$', r'## \1', text, flags=re.MULTILINE)
        
        # Clean up excessive spacing in lists
        text = re.sub(r'^\s*\n(\s*•)', r'\1', text, flags=re.MULTILINE)
        
        # Fix job entries formatting
        text = re.sub(r'(\*\*[^*]+\*\*)\s*\n([^*\n]+)\s*\n([^*\n]+)', r'\1  \n\2 | \3', text)
        
        # Remove multiple consecutive line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def generate_pdf_base64(self, markdown_text: str) -> Optional[str]:
        """Generate PDF from markdown and return as base64 string"""
        try:
            # Preprocess markdown
            cleaned_markdown = self.preprocess_markdown(markdown_text)
            
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=['tables', 'nl2br'])
            html_content = md.convert(cleaned_markdown)
            
            # Create complete HTML document
            full_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>{self.css_styles}</style>
            </head>
            <body>
                {html_content}
            </body>
            </html>
            """
            
            # Generate PDF
            pdf_bytes = weasyprint.HTML(string=full_html).write_pdf()
            
            # Convert to base64
            if pdf_bytes:
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            else:
                raise Exception("PDF generation returned None")
            
            print(f"✅ Optimized PDF generated successfully! Size: {len(pdf_base64)} characters")
            return pdf_base64
            
        except Exception as e:
            print(f"❌ Error generating optimized PDF: {e}")
            return None

# Test the generator
if __name__ == "__main__":
    generator = OptimizedPDFGenerator()
    
    test_markdown = """
# John Doe

San Francisco, CA | (555) 123-4567 | john.doe@email.com  
[LinkedIn](https://linkedin.com/in/johndoe) | [GitHub](https://github.com/johndoe)

## Professional Summary

Experienced software engineer with 5+ years of expertise in full-stack development.

## Experience

**Senior Software Engineer**  
Tech Company Inc. | San Francisco, CA | 2022 - Present

• Led development of scalable web applications
• Improved system performance by 40%
• Mentored junior developers

## Education

**Bachelor of Science in Computer Science**  
University of California, Berkeley | 2018

## Skills

• **Programming:** Python, JavaScript, React, Node.js
• **Databases:** PostgreSQL, MongoDB
• **Cloud:** AWS, Docker, Kubernetes
    """
    
    pdf_data = generator.generate_pdf_base64(test_markdown)
    if pdf_data:
        print("✅ Test successful!")
    else:
        print("❌ Test failed!")