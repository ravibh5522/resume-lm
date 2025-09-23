"""
PDF Generator for Resume Live Preview
Converts markdown to A4 PDF with professional styling
"""

import base64
import io
from typing import Optional
import markdown2
from weasyprint import HTML, CSS


class ResumePDFGenerator:
    def __init__(self):
        self.css_styles = """
        @page {
            size: A4;
            margin: 1in 0.8in;
            @bottom-center {
                content: counter(page) " / " counter(pages);
                font-size: 10pt;
                color: #666;
            }
        }
        
        body {
            font-family: 'Arial', 'Helvetica', sans-serif;
            line-height: 1.6;
            color: #333;
            margin: 0;
            padding: 0;
            font-size: 11pt;
        }
        
        /* Header styles */
        h1 {
            font-size: 24pt;
            font-weight: bold;
            color: #1e3a8a;
            text-align: center;
            margin: 0 0 8pt 0;
            padding: 0;
        }
        
        h2 {
            font-size: 14pt;
            font-weight: bold;
            color: #1e3a8a;
            margin: 16pt 0 8pt 0;
            padding: 8pt 0 4pt 0;
            border-bottom: 2px solid #0d9488;
        }
        
        h3 {
            font-size: 12pt;
            font-weight: bold;
            color: #374151;
            margin: 12pt 0 6pt 0;
        }
        
        /* Contact info */
        .contact-info {
            text-align: center;
            color: #666;
            margin: 8pt 0 16pt 0;
            font-size: 10pt;
        }
        
        /* Experience and sections */
        .job-title {
            font-weight: bold;
            color: #1e3a8a;
            font-size: 12pt;
        }
        
        .company-info {
            color: #666;
            font-style: italic;
            margin: 2pt 0 8pt 0;
        }
        
        /* Lists */
        ul {
            margin: 8pt 0;
            padding-left: 20pt;
        }
        
        li {
            margin: 4pt 0;
            list-style-type: disc;
        }
        
        /* Emojis and special formatting */
        .emoji {
            font-size: 12pt;
            margin-right: 4pt;
        }
        
        /* Skills grid */
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 8pt;
            margin: 8pt 0;
        }
        
        /* Project styling */
        .project {
            margin: 12pt 0;
            padding: 8pt;
            background-color: #f8fafc;
            border-left: 3px solid #0d9488;
        }
        
        /* Links */
        a {
            color: #0d9488;
            text-decoration: none;
        }
        
        /* Horizontal rules */
        hr {
            border: none;
            border-top: 1px solid #e5e7eb;
            margin: 16pt 0;
        }
        
        /* Paragraphs */
        p {
            margin: 6pt 0;
            text-align: justify;
        }
        
        /* Bold text */
        strong, b {
            color: #1e3a8a;
            font-weight: bold;
        }
        
        /* Code and technical terms */
        code {
            background-color: #f1f5f9;
            padding: 1pt 3pt;
            border-radius: 2pt;
            font-family: 'Courier New', monospace;
            font-size: 9pt;
        }
        
        /* Section spacing */
        .section {
            margin: 16pt 0;
        }
        
        /* Achievements and certifications */
        .achievement {
            margin: 6pt 0;
            padding: 4pt 8pt;
            background-color: #fef3c7;
            border-left: 3px solid #f59e0b;
        }
        """
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with proper formatting"""
        # Clean up the markdown content
        cleaned_md = self._clean_markdown(markdown_content)
        
        # Convert markdown to HTML
        html_content = markdown2.markdown(
            cleaned_md,
            extras=[
                'fenced-code-blocks',
                'tables',
                'break-on-newline',
                'strike',
                'target-blank-links'
            ]
        )
        
        # Post-process HTML for better PDF rendering
        html_content = self._enhance_html(html_content)
        
        return html_content
    
    def _clean_markdown(self, content: str) -> str:
        """Clean and prepare markdown content for PDF conversion"""
        lines = content.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Convert emoji-style headers to proper markdown headers
            line = line.strip()
            
            # Handle emoji headers
            if line.startswith('🚀 ') or line.startswith('💼 ') or line.startswith('🎓 '):
                line = f"## {line}"
            elif line.startswith('⚡ ') or line.startswith('🔹 '):
                line = f"### {line}"
            
            # Handle bullet points with emoji
            if line.startswith('◆ '):
                line = line.replace('◆ ', '• ')
            
            # Handle contact info line (contains |)
            if ' | ' in line and not line.startswith('#'):
                line = f'<div class="contact-info">{line}</div>'
            
            cleaned_lines.append(line)
        
        return '\n'.join(cleaned_lines)
    
    def _enhance_html(self, html_content: str) -> str:
        """Enhance HTML for better PDF rendering"""
        # Wrap sections for better styling
        enhanced = html_content
        
        # Add proper document structure
        enhanced = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Resume</title>
        </head>
        <body>
            {enhanced}
        </body>
        </html>
        """
        
        return enhanced
    
    def generate_pdf_base64(self, markdown_content: str) -> str:
        """Generate PDF from markdown and return as base64 string"""
        try:
            # Convert markdown to HTML
            html_content = self.markdown_to_html(markdown_content)
            
            # Create PDF
            html_obj = HTML(string=html_content)
            css_obj = CSS(string=self.css_styles)
            
            # Generate PDF to bytes
            pdf_bytes = html_obj.write_pdf(stylesheets=[css_obj])
            
            # Convert to base64
            if pdf_bytes:
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            else:
                return self._generate_error_pdf()
            
            return pdf_base64
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            # Return a minimal error PDF
            return self._generate_error_pdf()
    
    def _generate_error_pdf(self) -> str:
        """Generate a simple error PDF"""
        error_html = """
        <!DOCTYPE html>
        <html>
        <head><title>Error</title></head>
        <body>
            <h1>PDF Generation Error</h1>
            <p>Unable to generate PDF. Please check the resume content.</p>
        </body>
        </html>
        """
        
        try:
            html_obj = HTML(string=error_html)
            css_obj = CSS(string=self.css_styles)
            pdf_bytes = html_obj.write_pdf(stylesheets=[css_obj])
            if pdf_bytes:
                return base64.b64encode(pdf_bytes).decode('utf-8')
            else:
                return ""
        except:
            return ""


# Singleton instance
pdf_generator = ResumePDFGenerator()


def generate_resume_pdf_base64(markdown_content: str) -> str:
    """Generate PDF from markdown resume content"""
    return pdf_generator.generate_pdf_base64(markdown_content)


# Test function
if __name__ == "__main__":
    sample_markdown = """
# John Doe

San Francisco, CA | (555) 123-4567 | john@example.com

## 🚀 Professional Summary

Experienced software engineer with 5+ years in web development.

## 💼 Professional Experience

### Senior Developer
**Tech Company** | 2022-Present

• Developed scalable web applications
• Led team of 5 engineers
• Implemented CI/CD pipelines

## 🎓 Education

**Bachelor of Computer Science**
University of California | 2018

## ⚡ Skills

• Python, JavaScript, React
• AWS, Docker, Kubernetes
• Agile methodologies
"""
    
    pdf_base64 = generate_resume_pdf_base64(sample_markdown)
    print(f"Generated PDF (first 100 chars): {pdf_base64[:100]}...")
