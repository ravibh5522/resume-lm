"""
Advanced PDF Generator for Resume Markdown
Converts markdown resume content to A4 PDF format with proper formatting preservation
"""

import base64
import re
from io import BytesIO
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import markdown
from markdown.extensions import tables, nl2br, fenced_code

class AdvancedPDFGenerator:
    def __init__(self):
        self.font_config = FontConfiguration()
        
        # Initialize markdown parser with extensions
        self.md = markdown.Markdown(extensions=[
            'tables',
            'nl2br', 
            'fenced_code',
            'attr_list',
            'def_list'
        ])
        
    def markdown_to_pdf(self, markdown_content: str) -> bytes:
        """Convert markdown content to PDF bytes with advanced formatting"""
        try:
            # Pre-process markdown for better conversion
            processed_markdown = self._preprocess_markdown(markdown_content)
            
            # Convert markdown to HTML using proper parser
            html_content = self._markdown_to_html(processed_markdown)
            
            # Generate PDF with custom CSS
            pdf_bytes = self._html_to_pdf(html_content)
            return pdf_bytes
            
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return self._generate_error_pdf()
    
    def _preprocess_markdown(self, markdown_content: str) -> str:
        """Preprocess markdown to handle special formatting and preserve structure"""
        processed = markdown_content
        
        # Handle emoji symbols (convert to Unicode-safe symbols)
        emoji_map = {
            '🚀': '★',
            '💼': '■',
            '🎓': '▲',
            '⚡': '►',
            '🔹': '•',
            '📜': '■',
            '🏅': '★',
            '🌍': '●',
            '🔧': '►',
            '👤': '►',
            '📄': '►',
            '◆': '•',
            '🚀': '★'
        }
        
        for emoji, replacement in emoji_map.items():
            processed = processed.replace(emoji, replacement)
        
        # Convert horizontal rules to section breaks
        processed = re.sub(r'^---+\s*$', '\n<div class="section-break"></div>\n', processed, flags=re.MULTILINE)
        
        # Handle special bullet formatting
        processed = re.sub(r'^◆\s+(.+)$', r'* \1', processed, flags=re.MULTILINE)
        processed = re.sub(r'^▸\s+(.+)$', r'  * \1', processed, flags=re.MULTILINE)
        processed = re.sub(r'^►\s+(.+)$', r'  * \1', processed, flags=re.MULTILINE)
        
        # Handle contact info formatting (lines with | separators)
        contact_pattern = r'^(.+)\s+\|\s+(.+)\s+\|\s+(.+)$'
        processed = re.sub(contact_pattern, r'<div class="contact-info">\1 | \2 | \3</div>', processed, flags=re.MULTILINE)
        
        # Handle links in brackets 
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        processed = re.sub(link_pattern, r'<a href="\2">\1</a>', processed)
        
        # Handle job titles and company info
        job_pattern = r'^([A-Za-z ]+)\n([A-Za-z0-9 ,.]+)\s+\|\s+([A-Za-z0-9 ,.]+)\n([A-Za-z0-9 –-]+)\s*$'
        processed = re.sub(job_pattern, 
                          r'<div class="job-entry"><div class="job-title">\1</div><div class="company-info">\2 | \3</div><div class="date-range">\4</div></div>', 
                          processed, flags=re.MULTILINE)
        
        return processed
    
    def _markdown_to_html(self, markdown_content: str) -> str:
        """Convert markdown to HTML with comprehensive styling"""
        # Convert markdown to HTML
        html_body = self.md.convert(markdown_content)
        
        # Post-process HTML for better formatting
        html_body = self._postprocess_html(html_body)
        
        # Wrap in complete HTML document with advanced CSS
        html = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Resume</title>
            <style>
                @page {{
                    size: A4;
                    margin: 0.75in;
                    @bottom-center {{
                        content: counter(page) " of " counter(pages);
                        font-size: 8pt;
                        color: #888;
                    }}
                }}
                
                * {{
                    box-sizing: border-box;
                }}
                
                body {{ 
                    font-family: 'Segoe UI', 'Calibri', 'Arial', sans-serif; 
                    line-height: 1.5; 
                    margin: 0;
                    padding: 0;
                    font-size: 10pt;
                    color: #2d3748;
                    background: white;
                }}
                
                /* Name/Header */
                h1 {{ 
                    color: #1a365d; 
                    font-size: 24pt; 
                    margin: 0 0 12pt 0;
                    text-align: center;
                    font-weight: 700;
                    letter-spacing: 0.5pt;
                    border-bottom: 3px solid #2b6cb0;
                    padding-bottom: 8pt;
                }}
                
                /* Section Headers */
                h2 {{ 
                    color: #2b6cb0; 
                    font-size: 13pt; 
                    margin: 16pt 0 8pt 0;
                    font-weight: 600;
                    text-transform: uppercase;
                    letter-spacing: 0.5pt;
                    border-left: 4px solid #3182ce;
                    padding-left: 10pt;
                    background: linear-gradient(90deg, #ebf8ff 0%, transparent 100%);
                    padding-top: 4pt;
                    padding-bottom: 4pt;
                }}
                
                h3 {{ 
                    color: #4a5568; 
                    font-size: 11pt; 
                    margin: 12pt 0 6pt 0;
                    font-weight: 600;
                }}
                
                /* Contact Information */
                .contact-info {{
                    text-align: center;
                    margin: 0 0 20pt 0;
                    font-size: 9pt;
                    color: #718096;
                    padding: 8pt;
                    background: #f7fafc;
                    border-radius: 4pt;
                }}
                
                /* Job Entries */
                .job-entry {{
                    margin: 12pt 0;
                    padding: 8pt 0;
                    border-bottom: 1px solid #e2e8f0;
                }}
                
                .job-title {{
                    font-weight: 600;
                    font-size: 11pt;
                    color: #2d3748;
                    margin-bottom: 2pt;
                }}
                
                .company-info {{
                    color: #4a5568;
                    font-size: 9pt;
                    margin-bottom: 2pt;
                }}
                
                .date-range {{
                    color: #718096;
                    font-size: 9pt;
                    font-style: italic;
                }}
                
                /* Links */
                a {{
                    color: #3182ce;
                    text-decoration: none;
                    font-weight: 500;
                }}
                
                a:hover {{
                    text-decoration: underline;
                }}
                
                /* Lists */
                ul {{
                    margin: 6pt 0;
                    padding-left: 18pt;
                }}
                
                li {{
                    margin: 3pt 0;
                    line-height: 1.4;
                }}
                
                /* Nested lists */
                ul ul {{
                    margin: 2pt 0;
                    padding-left: 16pt;
                }}
                
                ul ul li {{
                    margin: 1pt 0;
                    list-style-type: circle;
                }}
                
                /* Section breaks */
                .section-break {{
                    border-top: 1px solid #cbd5e0;
                    margin: 16pt 0;
                    height: 1px;
                }}
                
                /* Tables */
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 8pt 0;
                    font-size: 9pt;
                }}
                
                th, td {{
                    text-align: left;
                    padding: 6pt 8pt;
                    border: 1px solid #e2e8f0;
                }}
                
                th {{
                    background-color: #edf2f7;
                    font-weight: 600;
                    color: #4a5568;
                }}
                
                /* Text formatting */
                strong, b {{
                    color: #2d3748;
                    font-weight: 600;
                }}
                
                em, i {{
                    color: #4a5568;
                    font-style: italic;
                }}
                
                /* Paragraph spacing */
                p {{
                    margin: 6pt 0;
                    text-align: justify;
                }}
                
                /* Code formatting */
                code {{
                    background-color: #edf2f7;
                    padding: 2pt 4pt;
                    border-radius: 3pt;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 8pt;
                    color: #e53e3e;
                }}
                
                /* Blockquotes */
                blockquote {{
                    margin: 12pt 0;
                    padding: 8pt 12pt;
                    border-left: 4px solid #3182ce;
                    background-color: #ebf8ff;
                    font-style: italic;
                    color: #2c5282;
                }}
                
                /* Skills sections */
                .skills-category {{
                    font-weight: 600;
                    color: #2d3748;
                    margin-top: 8pt;
                    margin-bottom: 4pt;
                }}
                
                /* Project formatting */
                .project-title {{
                    font-weight: 600;
                    color: #2d3748;
                    font-size: 10pt;
                }}
                
                .project-tech {{
                    color: #4a5568;
                    font-style: italic;
                    font-size: 9pt;
                }}
                
                /* Prevent orphans and widows */
                h1, h2, h3 {{
                    page-break-after: avoid;
                }}
                
                .job-entry {{
                    page-break-inside: avoid;
                }}
                
                /* Print optimizations */
                @media print {{
                    body {{
                        -webkit-print-color-adjust: exact;
                        print-color-adjust: exact;
                    }}
                }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        return html
    
    def _postprocess_html(self, html_content: str) -> str:
        """Post-process HTML for better formatting"""
        # Handle special formatting patterns
        processed = html_content
        
        # Better handling of GPA formatting
        processed = re.sub(r'_GPA:\s*([\d.]+/[\d.]+)_', r'<em>GPA: \1</em>', processed)
        
        # Handle skill categories with bullet points
        processed = re.sub(r'<p>([^:]+):<br\s*/?>([^<]+)</p>', 
                          r'<div class="skills-category">\1:</div><p>\2</p>', processed)
        
        return processed
    
    def _html_to_pdf(self, html_content: str) -> bytes:
        """Convert HTML to PDF bytes"""
        html_doc = HTML(string=html_content, base_url='')
        pdf_result = html_doc.write_pdf(font_config=self.font_config)
        return pdf_result if pdf_result is not None else b''
    
    def _generate_error_pdf(self) -> bytes:
        """Generate an error PDF when conversion fails"""
        error_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; padding: 40px; text-align: center; }
                .error { color: #e53e3e; font-size: 18pt; margin-bottom: 20px; }
                .message { color: #4a5568; font-size: 12pt; }
            </style>
        </head>
        <body>
            <div class="error">⚠️ PDF Generation Error</div>
            <div class="message">Unable to generate PDF from resume content.<br/>Please try refreshing or contact support.</div>
        </body>
        </html>
        """
        html_doc = HTML(string=error_html)
        pdf_result = html_doc.write_pdf()
        return pdf_result if pdf_result is not None else b''
    
    def get_base64_pdf(self, markdown_content: str) -> str:
        """Convert markdown to base64 encoded PDF string"""
        pdf_bytes = self.markdown_to_pdf(markdown_content)
        return base64.b64encode(pdf_bytes).decode('utf-8')