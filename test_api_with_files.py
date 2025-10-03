#!/usr/bin/env python3
"""
Test the updated chat API with file attachments
"""

import requests
import base64
import io
from PIL import Image

def create_test_image() -> str:
    """Create a simple test image and return as base64"""
    image = Image.new('RGB', (200, 100), color='blue')
    buffer = io.BytesIO()
    image.save(buffer, format='JPEG')
    image_bytes = buffer.getvalue()
    return base64.b64encode(image_bytes).decode('utf-8')

def test_api_integration():
    """Test the complete API with file attachments"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 TESTING UPDATED CHAT API WITH FILE ATTACHMENTS")
    print("=" * 60)
    
    try:
        # 1. Create session
        print("\n📱 Creating session...")
        response = requests.post(f"{base_url}/create-session")
        if response.status_code != 200:
            print(f"❌ Failed to create session: {response.status_code}")
            return False
        
        session_data = response.json()
        session_id = session_data["session_id"]
        print(f"✅ Session created: {session_id}")
        
        # 2. Test basic message (no attachments)
        print("\n💬 Testing basic message...")
        basic_request = {
            "session_id": session_id,
            "message": "Hi, I'm a software engineer with 3 years of experience",
            "attachments": []
        }
        
        response = requests.post(f"{base_url}/chat", json=basic_request)
        if response.status_code != 200:
            print(f"❌ Basic message failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        basic_response = response.json()
        print(f"✅ Basic message successful!")
        print(f"   AI Response: {basic_response['message'][:100]}...")
        
        # 3. Test message with image attachment
        print("\n🖼️ Testing message with image attachment...")
        
        image_base64 = create_test_image()
        
        image_request = {
            "session_id": session_id,
            "message": "Here's my profile photo for the resume",
            "attachments": [
                {
                    "filename": "profile_photo.jpg",
                    "file_type": "image",
                    "content": image_base64,
                    "mime_type": "image/jpeg"
                }
            ]
        }
        
        response = requests.post(f"{base_url}/chat", json=image_request)
        if response.status_code != 200:
            print(f"❌ Image attachment failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        image_response = response.json()
        print(f"✅ Image attachment successful!")
        print(f"   AI Response: {image_response['message'][:100]}...")
        
        # 4. Test multiple attachments
        print("\n📎 Testing multiple attachments...")
        
        # Create another test image
        image2_base64 = create_test_image()
        
        multi_request = {
            "session_id": session_id,
            "message": "Here are some additional photos",
            "attachments": [
                {
                    "filename": "photo1.png",
                    "file_type": "image",
                    "content": image_base64,
                    "mime_type": "image/png"
                },
                {
                    "filename": "photo2.png",
                    "file_type": "image", 
                    "content": image2_base64,
                    "mime_type": "image/png"
                }
            ]
        }
        
        response = requests.post(f"{base_url}/chat", json=multi_request)
        if response.status_code != 200:
            print(f"❌ Multiple attachments failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
        
        multi_response = response.json()
        print(f"✅ Multiple attachments successful!")
        print(f"   AI Response: {multi_response['message'][:100]}...")
        
        print(f"\n🎉 ALL API TESTS PASSED!")
        print(f"   ✓ Basic messaging works")
        print(f"   ✓ Image attachments work")
        print(f"   ✓ Multiple attachments work")
        print(f"   ✓ File processing integration successful")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Cannot connect to server at {base_url}")
        print(f"   Make sure the server is running with: python main.py")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

def print_usage_examples():
    """Print usage examples for developers"""
    print(f"\n📖 USAGE EXAMPLES FOR REACT DEVELOPERS:")
    print("=" * 50)
    
    print("""
// Basic message
const response = await fetch('/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    message: "I'm a software engineer",
    attachments: []
  })
});

// Message with PDF resume
const response = await fetch('/chat', {
  method: 'POST', 
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    message: "Please analyze my existing resume",
    attachments: [{
      filename: "my_resume.pdf",
      file_type: "pdf",
      content: base64PdfContent,
      mime_type: "application/pdf"
    }]
  })
});

// Message with profile photo
const response = await fetch('/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    session_id: sessionId,
    message: "Add this photo to my resume",
    attachments: [{
      filename: "profile.jpg",
      file_type: "image",
      content: base64ImageContent,
      mime_type: "image/jpeg"
    }]
  })
});
""")

if __name__ == "__main__":
    success = test_api_integration()
    print_usage_examples()
    
    if success:
        print(f"\n✅ API with file attachments is ready for production!")
    else:
        print(f"\n❌ Please fix the issues above before using in production.")