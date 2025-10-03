#!/usr/bin/env python3
"""
File Processing Utilities
Handles image and PDF processing for chat messages
"""

import base64
import io
import tempfile
import os
from typing import Optional, Tuple, List
from PIL import Image

# Try to import PDF libraries (will install them later)
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PyPDF2 = None
    PYPDF2_AVAILABLE = False

try:
    import fitz  # PyMuPDF
    PYMUPDF_AVAILABLE = True
except ImportError:
    fitz = None
    PYMUPDF_AVAILABLE = False

from models import FileAttachment

class FileProcessor:
    """
    Handles processing of uploaded images and PDFs for chat integration
    """
    
    def __init__(self):
        self.supported_image_types = {
            'image/jpeg', 'image/jpg', 'image/png', 'image/gif', 
            'image/bmp', 'image/webp', 'image/tiff'
        }
        self.supported_pdf_types = {'application/pdf'}
        
    def is_supported_file(self, mime_type: str) -> bool:
        """Check if file type is supported"""
        return mime_type in self.supported_image_types or mime_type in self.supported_pdf_types
    
    def process_attachment(self, attachment: FileAttachment) -> FileAttachment:
        """
        Process a file attachment (extract text from PDFs, validate images)
        
        Args:
            attachment: FileAttachment object with base64 content
            
        Returns:
            Processed FileAttachment with extracted text if applicable
        """
        if not self.is_supported_file(attachment.mime_type):
            raise ValueError(f"Unsupported file type: {attachment.mime_type}")
        
        if attachment.mime_type in self.supported_pdf_types:
            # Process PDF - extract text
            extracted_text = self.extract_pdf_text(attachment.content)
            attachment.extracted_text = extracted_text
            attachment.file_type = 'pdf'
            print(f"📄 Extracted {len(extracted_text)} characters from PDF: {attachment.filename}")
            
        elif attachment.mime_type in self.supported_image_types:
            # Process image - validate and optimize
            attachment.file_type = 'image'
            attachment = self.process_image(attachment)
            print(f"🖼️ Processed image: {attachment.filename}")
        
        return attachment
    
    def extract_pdf_text(self, base64_content: str) -> str:
        """
        Extract text from PDF using available libraries
        
        Args:
            base64_content: Base64 encoded PDF content
            
        Returns:
            Extracted text from PDF
        """
        try:
            # Decode base64 content
            pdf_bytes = base64.b64decode(base64_content)
            
            # Try PyMuPDF first (better results)
            if PYMUPDF_AVAILABLE:
                try:
                    return self._extract_pdf_pymupdf(pdf_bytes)
                except Exception as e:
                    print(f"⚠️ PyMuPDF extraction failed: {e}, trying PyPDF2...")
            
            # Fallback to PyPDF2
            if PYPDF2_AVAILABLE:
                try:
                    return self._extract_pdf_pypdf2(pdf_bytes)
                except Exception as e:
                    print(f"⚠️ PyPDF2 extraction failed: {e}")
            
            return "[PDF libraries not available - please install PyPDF2 or PyMuPDF]"
            
        except Exception as e:
            print(f"❌ PDF text extraction failed: {e}")
            return "[Unable to extract text from PDF]"
    
    def _extract_pdf_pymupdf(self, pdf_bytes: bytes) -> str:
        """Extract text using PyMuPDF (better quality)"""
        # Create temporary file for PyMuPDF
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_file.write(pdf_bytes)
            temp_file_path = temp_file.name
        
        try:
            # Extract text using PyMuPDF
            doc = fitz.open(temp_file_path)
            extracted_text = ""
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                extracted_text += f"\n--- Page {page_num + 1} ---\n"
                extracted_text += page_text
            
            doc.close()
            return extracted_text.strip()
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    def _extract_pdf_pypdf2(self, pdf_bytes: bytes) -> str:
        """Fallback PDF text extraction using PyPDF2"""
        try:
            pdf_file = io.BytesIO(pdf_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            extracted_text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                page_text = page.extract_text()
                extracted_text += f"\n--- Page {page_num + 1} ---\n"
                extracted_text += page_text
            
            return extracted_text.strip()
            
        except Exception as e:
            print(f"❌ PyPDF2 extraction failed: {e}")
            return "[Unable to extract text from PDF using PyPDF2]"
    
    def process_image(self, attachment: FileAttachment) -> FileAttachment:
        """
        Process and validate image
        
        Args:
            attachment: FileAttachment with image content
            
        Returns:
            Processed FileAttachment
        """
        try:
            # Decode base64 image
            image_bytes = base64.b64decode(attachment.content)
            
            # Open and validate image
            image = Image.open(io.BytesIO(image_bytes))
            
            # Get image info
            width, height = image.size
            format_type = image.format
            
            print(f"🖼️ Image processed: {width}x{height} {format_type}")
            
            # Optimize image if too large (optional)
            if width > 2048 or height > 2048:
                # Resize while maintaining aspect ratio
                image.thumbnail((2048, 2048), Image.Resampling.LANCZOS)
                
                # Re-encode to base64
                output_buffer = io.BytesIO()
                image.save(output_buffer, format=format_type or 'JPEG')
                attachment.content = base64.b64encode(output_buffer.getvalue()).decode('utf-8')
                
                print(f"🔧 Image resized to: {image.size}")
            
            return attachment
            
        except Exception as e:
            print(f"❌ Image processing failed: {e}")
            raise ValueError(f"Invalid image file: {e}")
    
    def prepare_for_ai(self, attachments: List[FileAttachment]) -> Tuple[List[str], List[str]]:
        """
        Prepare attachments for AI processing
        
        Args:
            attachments: List of processed FileAttachment objects
            
        Returns:
            Tuple of (text_content_list, image_base64_list) for AI
        """
        text_content = []
        image_content = []
        
        for attachment in attachments:
            if attachment.file_type == 'pdf' and attachment.extracted_text:
                text_content.append(
                    f"📄 Content from '{attachment.filename}':\n{attachment.extracted_text}"
                )
            elif attachment.file_type == 'image':
                image_content.append(attachment.content)
                text_content.append(
                    f"🖼️ Image uploaded: '{attachment.filename}' ({attachment.mime_type})"
                )
        
        return text_content, image_content
    
    def get_mime_type_from_extension(self, filename: str) -> Optional[str]:
        """
        Get MIME type from file extension
        
        Args:
            filename: Name of the file
            
        Returns:
            MIME type string or None
        """
        extension = filename.lower().split('.')[-1]
        
        mime_types = {
            'pdf': 'application/pdf',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'bmp': 'image/bmp',
            'webp': 'image/webp',
            'tiff': 'image/tiff',
            'tif': 'image/tiff'
        }
        
        return mime_types.get(extension)

# Global instance
file_processor = FileProcessor()

# Helper functions for easy import
def process_file_attachment(attachment: FileAttachment) -> FileAttachment:
    """Process a single file attachment"""
    return file_processor.process_attachment(attachment)

def extract_text_from_pdf(base64_content: str) -> str:
    """Extract text from PDF base64 content"""
    return file_processor.extract_pdf_text(base64_content)

def prepare_attachments_for_ai(attachments: List[FileAttachment]) -> Tuple[List[str], List[str]]:
    """Prepare attachments for AI processing"""
    return file_processor.prepare_for_ai(attachments)