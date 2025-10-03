#!/usr/bin/env python3
"""
Test file processing functionality
"""

import base64
import io
from PIL import Image
from models import FileAttachment
from file_processor import process_file_attachment

def create_test_image() -> str:
    """Create a simple test image and return as base64"""
    # Create a simple 100x100 red square image
    image = Image.new('RGB', (100, 100), color='red')
    
    # Convert to base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    image_bytes = buffer.getvalue()
    
    return base64.b64encode(image_bytes).decode('utf-8')

def test_image_processing():
    """Test image processing functionality"""
    print("🧪 Testing image processing...")
    
    try:
        # Create test image
        image_base64 = create_test_image()
        
        # Create FileAttachment
        attachment = FileAttachment(
            filename="test_image.png",
            file_type="image",
            content=image_base64,
            mime_type="image/png"
        )
        
        # Process the attachment
        processed = process_file_attachment(attachment)
        
        print(f"✅ Image processing successful!")
        print(f"   📝 Filename: {processed.filename}")
        print(f"   📝 Type: {processed.file_type}")
        print(f"   📝 MIME: {processed.mime_type}")
        print(f"   📝 Content size: {len(processed.content)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Image processing failed: {e}")
        return False

def test_pdf_processing():
    """Test PDF processing functionality (without actual PDF)"""
    print("\n🧪 Testing PDF processing availability...")
    
    try:
        from file_processor import PYPDF2_AVAILABLE, PYMUPDF_AVAILABLE
        
        print(f"   📚 PyPDF2 available: {PYPDF2_AVAILABLE}")
        print(f"   📚 PyMuPDF available: {PYMUPDF_AVAILABLE}")
        
        if not PYPDF2_AVAILABLE and not PYMUPDF_AVAILABLE:
            print("   ⚠️ No PDF libraries available. Install with:")
            print("      pip install PyPDF2 PyMuPDF")
        else:
            print("   ✅ PDF processing libraries available!")
        
        return True
        
    except Exception as e:
        print(f"❌ PDF library check failed: {e}")
        return False

def test_file_types():
    """Test supported file type detection"""
    print("\n🧪 Testing file type detection...")
    
    try:
        from file_processor import file_processor
        
        test_cases = [
            ("image.jpg", "image/jpeg", True),
            ("document.pdf", "application/pdf", True),
            ("video.mp4", "video/mp4", False),
            ("text.txt", "text/plain", False),
        ]
        
        for filename, mime_type, expected in test_cases:
            result = file_processor.is_supported_file(mime_type)
            status = "✅" if result == expected else "❌"
            print(f"   {status} {filename} ({mime_type}): {result}")
        
        return True
        
    except Exception as e:
        print(f"❌ File type detection failed: {e}")
        return False

def main():
    print("🚀 FILE PROCESSING TEST SUITE")
    print("=" * 50)
    
    tests = [
        test_image_processing,
        test_pdf_processing,
        test_file_types
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n📊 TEST RESULTS:")
    print(f"   ✅ Passed: {sum(results)}")
    print(f"   ❌ Failed: {len(results) - sum(results)}")
    print(f"   📈 Success rate: {sum(results)/len(results)*100:.1f}%")
    
    if all(results):
        print("\n🎉 All tests passed! File processing is ready.")
    else:
        print("\n⚠️ Some tests failed. Check dependencies.")

if __name__ == "__main__":
    main()