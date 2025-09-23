#!/usr/bin/env python3
"""
Ultra Advanced PDF Generator with Perfect Markdown Parsing
Handles complex markdown structures, proper spacing, and professional formatting
"""

import markdown
from markdown.extensions import tables, codehilite, toc
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import base64
import re
from typing import Optional
import html

class UltraAdvancedPDFGenerator:
    def __init__(self):
        self.font_config = FontConfiguration()
        
    def preprocess_markdown(self, markdown_content: str) -> str:
        """Advanced markdown preprocessing to fix common formatting issues"""
        
        # Clean up excessive whitespace but preserve intentional spacing
        lines = markdown_content.split('\n')
        processed_lines = []
        
        for i, line in enumerate(lines):
            # Remove trailing whitespace
            line = line.rstrip()
            
            # Handle headers with proper spacing
            if line.startswith('#'):
                # Add space before headers (except first line)
                if i > 0 and processed_lines and processed_lines[-1].strip():
                    processed_lines.append('')
                processed_lines.append(line)
                processed_lines.append('')  # Add space after headers
                continue
            
            # Handle list items with better formatting
            if re.match(r'^[\s]*[•◆⚡🔹▸\-\*\+]\s', line):
                # Ensure proper indentation for list items
                indent_match = re.match(r'^(\s*)', line)
                indent = indent_match.group(1) if indent_match else ''
                bullet_match = re.match(r'^[\s]*([•◆⚡🔹▸\-\*\+])\s*(.*)', line)
                if bullet_match:
                    bullet, content = bullet_match.groups()
                    # Standardize bullet points
                    if bullet in ['•', '◆', '⚡', '🔹', '▸']:
                        line = f"{indent}• {content}"
                    else:
                        line = f"{indent}• {content}"
            
            # Handle horizontal rules
            if line.strip() in ['---', '***', '___']:
                if processed_lines and processed_lines[-1].strip():
                    processed_lines.append('')
                processed_lines.append('---')
                processed_lines.append('')
                continue
            
            # Handle table formatting
            if '|' in line and not line.strip().startswith('|'):
                # Ensure tables start with |
                if not line.strip().startswith('|'):
                    line = '| ' + line.strip() + ' |'
            
            processed_lines.append(line)
        
        # Join and clean up excessive blank lines
        content = '\n'.join(processed_lines)
        content = re.sub(r'\n{3,}', '\n\n', content)  # Max 2 consecutive newlines
        
        return content
    
    def get_advanced_css(self) -> str:
        """Ultra advanced CSS for perfect resume formatting"""
        return """
        @page {
            size: A4;
            margin: 0.75in 0.75in 0.75in 0.75in;
            @top-center {
                content: none;
            }
            @bottom-center {
                content: counter(page) " of " counter(pages);
                font-size: 10px;
                color: #666;
            }
        }
        
        * {
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11px;
            line-height: 1.4;
            color: #2c3e50;
            margin: 0;
            padding: 0;
            background: white;
        }
        
        /* Header Styles */
        h1 {
            font-size: 28px;
            font-weight: 700;
            color: #2980b9;
            text-align: center;
            margin: 0 0 8px 0;
            padding: 0;
            letter-spacing: 1px;
        }
        
        h2 {
            font-size: 16px;
            font-weight: 600;
            color: #2980b9;
            margin: 20px 0 8px 0;
            padding: 6px 0 6px 12px;
            border-left: 4px solid #3498db;
            background: linear-gradient(90deg, #ecf0f1 0%, transparent 100%);
            page-break-after: avoid;
        }
        
        h3 {
            font-size: 14px;
            font-weight: 600;
            color: #34495e;
            margin: 12px 0 6px 0;
            page-break-after: avoid;
        }
        
        h4 {
            font-size: 12px;
            font-weight: 600;
            color: #7f8c8d;
            margin: 8px 0 4px 0;
            page-break-after: avoid;
        }
        
        /* Contact Information Styling */
        p:first-of-type {
            text-align: center;
            font-size: 12px;
            color: #7f8c8d;
            margin: 8px 0 16px 0;
            line-height: 1.6;
        }
        
        /* Paragraph Styles */
        p {
            margin: 8px 0;
            text-align: justify;
            orphans: 2;
            widows: 2;
        }
        
        /* List Styles */
        ul, ol {
            margin: 8px 0 12px 0;
            padding-left: 20px;
        }
        
        li {
            margin: 4px 0;
            line-height: 1.5;
            page-break-inside: avoid;
        }
        
        ul li {
            list-style-type: none;
            position: relative;
            padding-left: 16px;
        }
        
        ul li:before {
            content: "•";
            color: #3498db;
            font-weight: bold;
            position: absolute;
            left: 0;
            top: 0;
        }
        
        /* Nested lists */
        ul ul li:before {
            content: "◦";
            color: #95a5a6;
        }
        
        /* Table Styles */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 11px;
            page-break-inside: avoid;
        }
        
        th {
            background: #3498db;
            color: white;
            padding: 8px 12px;
            text-align: left;
            font-weight: 600;
            border: 1px solid #2980b9;
        }
        
        td {
            padding: 6px 12px;
            border: 1px solid #bdc3c7;
            vertical-align: top;
        }
        
        tr:nth-child(even) td {
            background: #f8f9fa;
        }
        
        /* Horizontal Rules */
        hr {
            border: none;
            height: 2px;
            background: linear-gradient(90deg, #3498db, transparent);
            margin: 16px 0;
        }
        
        /* Links */
        a {
            color: #3498db;
            text-decoration: none;
        }
        
        a:hover {
            text-decoration: underline;
        }
        
        /* Code and Technical Elements */
        code {
            background: #ecf0f1;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 10px;
        }
        
        /* Strong and Emphasis */
        strong, b {
            font-weight: 600;
            color: #2c3e50;
        }
        
        em, i {
            font-style: italic;
            color: #34495e;
        }
        
        /* Page Break Control */
        .page-break {
            page-break-before: always;
        }
        
        .no-break {
            page-break-inside: avoid;
        }
        
        /* Section Spacing */
        .section {
            margin-bottom: 16px;
            page-break-inside: avoid;
        }
        
        /* Professional Spacing */
        .contact-info {
            text-align: center;
            margin: 8px 0 20px 0;
            font-size: 12px;
            color: #7f8c8d;
        }
        
        .contact-info a {
            color: #3498db;
            text-decoration: none;
            margin: 0 8px;
        }
        
        /* Special Elements */
        blockquote {
            border-left: 4px solid #3498db;
            margin: 12px 0;
            padding: 8px 16px;
            background: #f8f9fa;
            font-style: italic;
        }
        
        /* Fix for markdown artifacts */
        .markdown-artifact {
            display: none;
        }
        
        /* Ensure proper spacing between sections */
        h2 + p, h2 + ul, h2 + ol, h2 + table {
            margin-top: 8px;
        }
        
        /* Print optimizations */
        @media print {
            body {
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }
        }
        """
    
    def post_process_html(self, html_content: str) -> str:
        """Post-process HTML to fix formatting issues"""
        
        # Fix contact information formatting
        html_content = re.sub(
            r'<p>([^<]*\|[^<]*)</p>',
            r'<p class="contact-info">\1</p>',
            html_content
        )
        
        # Wrap sections in divs for better spacing
        html_content = re.sub(
            r'(<h2[^>]*>.*?</h2>)',
            r'<div class="section">\1',
            html_content
        )
        
        # Close section divs before next h2 or end of content
        html_content = re.sub(
            r'</div>\s*(<div class="section">)',
            r'</div>\1',
            html_content
        )
        
        # Add closing div at the end if needed
        if '<div class="section">' in html_content and not html_content.endswith('</div>'):
            html_content += '</div>'
        
        # Clean up table formatting
        html_content = re.sub(
            r'<p>\s*\|([^|]+)\|([^|]+)\|([^|]+)\|\s*</p>',
            r'<table><tr><td>\1</td><td>\2</td><td>\3</td></tr></table>',
            html_content
        )
        
        # Fix list formatting issues
        html_content = re.sub(
            r'<p>([•◆⚡🔹▸])\s*(.*?)</p>',
            r'<ul><li>\2</li></ul>',
            html_content
        )
        
        # Merge consecutive ul tags
        html_content = re.sub(r'</ul>\s*<ul>', '', html_content)
        
        return html_content
    
    def markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with advanced parsing"""
        
        # Preprocess markdown
        processed_content = self.preprocess_markdown(markdown_content)
        
        # Configure markdown with extensions
        md = markdown.Markdown(
            extensions=[
                'tables',
                'fenced_code',
                'codehilite',
                'toc',
                'attr_list',
                'def_list',
                'footnotes',
                'md_in_html',
                'nl2br'
            ],
            extension_configs={
                'codehilite': {
                    'css_class': 'highlight',
                    'use_pygments': False
                },
                'toc': {
                    'anchorlink': False
                }
            }
        )
        
        # Convert to HTML
        html_content = md.convert(processed_content)
        
        # Post-process HTML
        html_content = self.post_process_html(html_content)
        
        return html_content
    
    def generate_pdf_base64(self, markdown_content: str) -> str:
        """Generate PDF from markdown with ultra-advanced formatting"""
        try:
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
            
            # Generate PDF
            html_doc = HTML(string=full_html)
            css_doc = CSS(string=self.get_advanced_css(), font_config=self.font_config)
            
            pdf_bytes = html_doc.write_pdf(stylesheets=[css_doc], font_config=self.font_config)
            
            # Convert to base64
            if pdf_bytes:
                pdf_base64 = base64.b64encode(pdf_bytes).decode('utf-8')
            else:
                pdf_base64 = ""
            
            return pdf_base64
            
        except Exception as e:
            print(f"PDF generation error: {e}")
            return ""

# Global instance
ultra_pdf_generator = UltraAdvancedPDFGenerator()

def generate_ultra_advanced_pdf_base64(markdown_content: str) -> str:
    """Generate PDF with ultra-advanced formatting"""
    return ultra_pdf_generator.generate_pdf_base64(markdown_content)