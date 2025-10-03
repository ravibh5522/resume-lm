# 🚀 AI Resume Generator - API & WebSocket Documentation

## Table of Contents
- [Overview](#overview)
- [Authentication](#authentication) 
- [REST API Endpoints](#rest-api-endpoints)
- [WebSocket Connection](#websocket-connection)
- [Data Models](#data-models)
- [React Integration Examples](#react-integration-examples)
- [Error Handling](#error-handling)
- [Rate Limiting](#rate-limiting)

## Overview

The AI Resume Generator provides a real-time API for building and modifying resumes using AI. It features:

- **Real-time updates** via WebSocket connections
- **Intelligent resume generation** from natural language input
- **Live resume modifications** without full regeneration
- **Multi-format output** (PDF, DOCX, Markdown)
- **Auto-fit formatting** for single-page layouts

**Base URL**: `http://localhost:8000` (development) or your deployed URL

---

## Authentication

Currently, the API uses **session-based authentication** with unique session IDs. No API keys required.

---

## REST API Endpoints

### 1. Create Session
Create a new chat session for resume building.

**`POST /create-session`**

**Request:**
```json
{}
```

**Response:**
```json
{
  "session_id": "uuid-v4-string"
}
```

**React Example:**
```javascript
const createSession = async () => {
  const response = await fetch('/create-session', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' }
  });
  const data = await response.json();
  return data.session_id;
};
```

---

### 2. Send Chat Message
Send a message to the AI for resume building or modification, with optional file attachments.

**`POST /chat`**

**Request:**
```json
{
  "session_id": "uuid-v4-string",
  "message": "I'm a senior software engineer with 5 years experience in React and Node.js",
  "attachments": [
    {
      "filename": "my_resume.pdf",
      "file_type": "pdf",
      "content": "base64-encoded-pdf-content",
      "mime_type": "application/pdf"
    },
    {
      "filename": "profile_photo.jpg",
      "file_type": "image", 
      "content": "base64-encoded-image-content",
      "mime_type": "image/jpeg"
    }
  ]
}
```

**Response:**
```json
{
  "message": "I've processed your PDF resume and will help you improve it. Can you tell me about any recent achievements?",
  "session_id": "uuid-v4-string"
}
```

**Supported File Types:**
- **PDFs**: `application/pdf` - Text will be extracted automatically
- **Images**: `image/jpeg`, `image/png`, `image/gif`, `image/bmp`, `image/webp`, `image/tiff`

**React Example:**
```javascript
const sendMessageWithFiles = async (sessionId, message, files = []) => {
  // Process files to base64
  const attachments = await Promise.all(files.map(async (file) => {
    const base64 = await fileToBase64(file);
    return {
      filename: file.name,
      file_type: file.type.startsWith('image/') ? 'image' : 'pdf',
      content: base64.split(',')[1], // Remove data:mime;base64, prefix
      mime_type: file.type
    };
  }));

  const response = await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      message: message,
      attachments: attachments
    })
  });
  return await response.json();
};

// Helper function to convert file to base64
const fileToBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });
};
```

---

### 3. Generate DOCX
Generate a DOCX file from resume markdown.

**`POST /generate-docx`**

**Request:**
```json
{
  "session_id": "uuid-v4-string",
  "markdown": "# John Smith\n\n## Experience\n..."
}
```

**Response:**
```json
{
  "docx_base64": "base64-encoded-docx-data",
  "session_id": "uuid-v4-string",
  "success": true,
  "error": null
}
```

**React Example:**
```javascript
const generateDocx = async (sessionId, markdown) => {
  const response = await fetch('/generate-docx', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      session_id: sessionId,
      markdown: markdown
    })
  });
  return await response.json();
};

// Download the DOCX file
const downloadDocx = (base64Data, filename = 'resume.docx') => {
  const byteCharacters = atob(base64Data);
  const byteNumbers = new Array(byteCharacters.length);
  for (let i = 0; i < byteCharacters.length; i++) {
    byteNumbers[i] = byteCharacters.charCodeAt(i);
  }
  const byteArray = new Uint8Array(byteNumbers);
  const blob = new Blob([byteArray], { 
    type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
  });
  
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
};
```

---

### 4. Get Session Data
Retrieve current session information.

**`GET /session/{session_id}`**

**Response:**
```json
{
  "session_id": "uuid-v4-string",
  "user_data": {
    "name": "John Smith",
    "email": "john@example.com",
    // ... other user data
  },
  "chat_history": [
    {
      "role": "user",
      "content": "I'm a software engineer",
      "timestamp": "2025-09-29T10:00:00Z"
    }
  ],
  "resume_markdown": "# John Smith\n...",
  "last_updated": "2025-09-29T10:00:00Z"
}
```

---

## WebSocket Connection

### Connection
Connect to real-time updates for a specific session.

**`WS /ws/{session_id}`**

**React Example:**
```javascript
const connectWebSocket = (sessionId, onMessage) => {
  const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
  
  ws.onopen = () => {
    console.log('WebSocket connected');
  };
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    onMessage(data);
  };
  
  ws.onclose = () => {
    console.log('WebSocket disconnected');
  };
  
  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };
  
  return ws;
};
```

### WebSocket Message Types

#### 1. Chat Response
AI response to user message.

```json
{
  "type": "chat_response",
  "message": "I'll help you build your resume. What's your current job title?",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

#### 2. Resume Generation Started
Resume generation has begun.

```json
{
  "type": "resume_generation_started",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

#### 3. Resume Generated
Complete resume has been generated (markdown format).

```json
{
  "type": "resume_generated",
  "resume_markdown": "# John Smith\n\nSenior Software Engineer...",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

#### 4. PDF Update
PDF version of resume is ready.

```json
{
  "type": "resume_pdf_update",
  "pdf_base64": "base64-encoded-pdf-data",
  "resume_markdown": "# John Smith\n...",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z",
  "modification_type": "minor" // "minor", "moderate", "major"
}
```

#### 5. DOCX Update
DOCX version of resume is ready.

```json
{
  "type": "resume_docx_update",
  "docx_base64": "base64-encoded-docx-data",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z",
  "modification_type": "minor"
}
```

#### 6. File Processing Messages
When files are processed successfully or fail.

**File Processing Success:**
```json
{
  "type": "chat_response",
  "message": "📎 Processed 2 files successfully!",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

**File Processing Error:**
```json
{
  "type": "error",
  "message": "Failed to process file 'resume.pdf': Unable to extract text from PDF",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

#### 7. Error Messages
When something goes wrong.

```json
{
  "type": "error",
  "message": "Failed to generate resume: insufficient data",
  "session_id": "uuid-v4-string",
  "timestamp": "2025-09-29T10:00:00Z"
}
```

---

## Data Models

### FileAttachment
```typescript
interface FileAttachment {
  filename: string;
  file_type: 'image' | 'pdf';
  content: string; // base64 encoded content
  mime_type: string; // e.g., 'image/jpeg', 'application/pdf'
  extracted_text?: string; // For PDFs only
}
```

### ChatMessage
```typescript
interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: string; // ISO datetime
  attachments: FileAttachment[]; // Optional file attachments
}
```

### ChatRequest
```typescript
interface ChatRequest {
  message: string;
  session_id: string;
  attachments: FileAttachment[]; // Optional file attachments
}
```

### UserProfile
```typescript
interface UserProfile {
  name?: string;
  email?: string;
  phone?: string;
  location?: string;
  linkedin?: string;
  github?: string;
  website?: string;
}
```

### Experience
```typescript
interface Experience {
  company: string;
  position: string;
  start_date: string;
  end_date?: string;
  description: string[];
}
```

### SessionData
```typescript
interface SessionData {
  session_id: string;
  user_data: UserProfile;
  chat_history: ChatMessage[];
  resume_markdown?: string;
  last_updated: string;
}
```

---

## React Integration Examples

### Complete React Hook for Resume Building

```javascript
import { useState, useEffect, useRef } from 'react';

const useResumeBuilder = () => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [resumeMarkdown, setResumeMarkdown] = useState('');
  const [resumePdf, setResumePdf] = useState(null);
  const [resumeDocx, setResumeDocx] = useState(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const wsRef = useRef(null);

  // Initialize session
  const initSession = async () => {
    try {
      const response = await fetch('/create-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      setSessionId(data.session_id);
      return data.session_id;
    } catch (error) {
      console.error('Failed to create session:', error);
      throw error;
    }
  };

  // Connect WebSocket
  const connectWebSocket = (sessionId) => {
    const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);
    
    ws.onopen = () => {
      setIsConnected(true);
      console.log('Connected to resume builder');
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      handleWebSocketMessage(data);
    };
    
    ws.onclose = () => {
      setIsConnected(false);
      console.log('Disconnected from resume builder');
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsConnected(false);
    };
    
    wsRef.current = ws;
    return ws;
  };

  // Handle WebSocket messages
  const handleWebSocketMessage = (data) => {
    switch (data.type) {
      case 'chat_response':
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.message,
          timestamp: data.timestamp
        }]);
        break;
        
      case 'resume_generation_started':
        setIsGenerating(true);
        break;
        
      case 'resume_generated':
        setResumeMarkdown(data.resume_markdown);
        setIsGenerating(false);
        break;
        
      case 'resume_pdf_update':
        setResumePdf(data.pdf_base64);
        setResumeMarkdown(data.resume_markdown);
        break;
        
      case 'resume_docx_update':
        setResumeDocx(data.docx_base64);
        break;
        
      case 'error':
        console.error('Resume builder error:', data.message);
        setIsGenerating(false);
        break;
        
      default:
        console.log('Unknown message type:', data.type);
    }
  };

  // Send message with optional file attachments
  const sendMessage = async (message, files = []) => {
    if (!sessionId) {
      throw new Error('No active session');
    }

    // Process files to attachments
    const attachments = await Promise.all(files.map(async (file) => {
      const base64 = await fileToBase64(file);
      return {
        filename: file.name,
        file_type: file.type.startsWith('image/') ? 'image' : 'pdf',
        content: base64.split(',')[1], // Remove data:mime;base64, prefix
        mime_type: file.type
      };
    }));

    // Add user message to UI immediately
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
      attachments: attachments
    }]);

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          message: message,
          attachments: attachments
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to send message');
      }
      
      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  };

  // Helper function to convert file to base64
  const fileToBase64 = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onload = () => resolve(reader.result);
      reader.onerror = error => reject(error);
    });
  };

  // Download PDF
  const downloadPdf = (filename = 'resume.pdf') => {
    if (!resumePdf) {
      throw new Error('No PDF available');
    }
    
    const byteCharacters = atob(resumePdf);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: 'application/pdf' });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Download DOCX
  const downloadDocx = (filename = 'resume.docx') => {
    if (!resumeDocx) {
      throw new Error('No DOCX available');
    }
    
    const byteCharacters = atob(resumeDocx);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { 
      type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
    });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Initialize on mount
  useEffect(() => {
    const init = async () => {
      try {
        const newSessionId = await initSession();
        connectWebSocket(newSessionId);
      } catch (error) {
        console.error('Failed to initialize resume builder:', error);
      }
    };
    
    init();
    
    // Cleanup
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  return {
    sessionId,
    messages,
    resumeMarkdown,
    resumePdf,
    resumeDocx,
    isConnected,
    isGenerating,
    sendMessage,
    downloadPdf,
    downloadDocx
  };
};

export default useResumeBuilder;
```

### React Component Example

```jsx
import React, { useState } from 'react';
import useResumeBuilder from './useResumeBuilder';

const ResumeBuilder = () => {
  const [inputMessage, setInputMessage] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const {
    messages,
    resumeMarkdown,
    resumePdf,
    resumeDocx,
    isConnected,
    isGenerating,
    sendMessage,
    downloadPdf,
    downloadDocx
  } = useResumeBuilder();

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputMessage.trim() && selectedFiles.length === 0) return;
    
    try {
      await sendMessage(inputMessage, selectedFiles);
      setInputMessage('');
      setSelectedFiles([]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    // Filter for supported file types
    const supportedFiles = files.filter(file => 
      file.type.startsWith('image/') || file.type === 'application/pdf'
    );
    setSelectedFiles(supportedFiles);
  };

  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className="resume-builder">
      <div className="status">
        <span className={`connection ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </span>
        {isGenerating && <span className="generating">🔄 Generating resume...</span>}
      </div>
      
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role === 'user' ? 'You' : 'AI'}:</strong>
            <span>{msg.content}</span>
            {msg.attachments && msg.attachments.length > 0 && (
              <div className="attachments">
                {msg.attachments.map((attachment, i) => (
                  <span key={i} className="attachment">
                    📎 {attachment.filename}
                  </span>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
      
      <form onSubmit={handleSendMessage} className="message-input">
        <div className="input-section">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            placeholder="Tell me about your experience, or upload your resume..."
            disabled={!isConnected}
          />
          
          <input
            type="file"
            multiple
            accept="image/*,.pdf"
            onChange={handleFileSelect}
            style={{ display: 'none' }}
            id="file-input"
          />
          
          <label htmlFor="file-input" className="file-button">
            📎 Files
          </label>
        </div>
        
        {selectedFiles.length > 0 && (
          <div className="selected-files">
            {selectedFiles.map((file, index) => (
              <div key={index} className="file-item">
                <span>{file.name}</span>
                <button type="button" onClick={() => removeFile(index)}>×</button>
              </div>
            ))}
          </div>
        )}
        
        <button type="submit" disabled={!isConnected || isGenerating}>
          Send
        </button>
      </form>
      
      {resumeMarkdown && (
        <div className="resume-preview">
          <h3>Resume Preview</h3>
          <pre>{resumeMarkdown}</pre>
          
          <div className="download-buttons">
            {resumePdf && (
              <button onClick={() => downloadPdf()}>
                📄 Download PDF
              </button>
            )}
            {resumeDocx && (
              <button onClick={() => downloadDocx()}>
                📝 Download DOCX
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default ResumeBuilder;
```

---

## Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid input)
- **404**: Session not found
- **500**: Internal server error

### Error Response Format
```json
{
  "detail": "Session not found",
  "status_code": 404
}
```

### WebSocket Error Handling
```javascript
ws.onerror = (error) => {
  console.error('WebSocket error:', error);
  // Implement reconnection logic
  setTimeout(() => {
    connectWebSocket(sessionId);
  }, 3000);
};
```

---

## Rate Limiting

Currently, there are no explicit rate limits, but consider implementing:
- **Message rate**: Max 10 messages per minute per session
- **File generation**: Max 5 PDF/DOCX generations per minute
- **Session creation**: Max 10 sessions per IP per hour

---

## Best Practices

### 1. Session Management
```javascript
// Store session ID in localStorage for persistence
localStorage.setItem('resume_session_id', sessionId);

// Restore session on page reload
const storedSessionId = localStorage.getItem('resume_session_id');
if (storedSessionId) {
  connectWebSocket(storedSessionId);
}
```

### 2. Error Handling
```javascript
// Always handle WebSocket reconnection
const reconnectWebSocket = () => {
  if (wsRef.current?.readyState === WebSocket.CLOSED) {
    setTimeout(() => {
      connectWebSocket(sessionId);
    }, 1000);
  }
};
```

### 3. File Downloads
```javascript
// Validate base64 data before download
const isValidBase64 = (str) => {
  try {
    return btoa(atob(str)) === str;
  } catch (err) {
    return false;
  }
};
```

### 4. Message Optimization
```javascript
// Debounce rapid messages
const debouncedSendMessage = debounce(sendMessage, 500);
```

---

## Support

For issues or questions about the API:
1. Check the console logs for detailed error messages
2. Verify WebSocket connection status
3. Ensure session ID is valid and active
4. Check network connectivity

The AI Resume Generator API is designed for real-time, interactive resume building with intelligent modification detection and multi-format output generation.
