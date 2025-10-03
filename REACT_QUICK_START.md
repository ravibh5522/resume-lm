# 🚀 Quick Start - React Integration Guide

## 1. Basic Setup (Copy & Paste Ready)

### Step 1: Create Resume Hook
```javascript
// hooks/useResumeBuilder.js
import { useState, useEffect, useRef } from 'react';

export const useResumeBuilder = (baseUrl = 'http://localhost:8000') => {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [resumeData, setResumeData] = useState({
    markdown: '',
    pdf: null,
    docx: null
  });
  const [status, setStatus] = useState({
    connected: false,
    generating: false,
    error: null
  });
  const wsRef = useRef(null);

  // Initialize session and WebSocket
  const initialize = async () => {
    try {
      // Create session
      const response = await fetch(`${baseUrl}/create-session`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await response.json();
      const newSessionId = data.session_id;
      setSessionId(newSessionId);

      // Connect WebSocket
      const wsUrl = baseUrl.replace('http', 'ws');
      const ws = new WebSocket(`${wsUrl}/ws/${newSessionId}`);
      
      ws.onopen = () => {
        setStatus(prev => ({ ...prev, connected: true, error: null }));
      };
      
      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleMessage(data);
      };
      
      ws.onclose = () => {
        setStatus(prev => ({ ...prev, connected: false }));
      };
      
      ws.onerror = (error) => {
        setStatus(prev => ({ ...prev, error: 'Connection failed' }));
      };
      
      wsRef.current = ws;
    } catch (error) {
      setStatus(prev => ({ ...prev, error: error.message }));
    }
  };

  // Handle WebSocket messages
  const handleMessage = (data) => {
    switch (data.type) {
      case 'chat_response':
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: data.message,
          timestamp: data.timestamp
        }]);
        break;
        
      case 'resume_generation_started':
        setStatus(prev => ({ ...prev, generating: true }));
        break;
        
      case 'resume_generated':
        setResumeData(prev => ({ ...prev, markdown: data.resume_markdown }));
        setStatus(prev => ({ ...prev, generating: false }));
        break;
        
      case 'resume_pdf_update':
        setResumeData(prev => ({ ...prev, pdf: data.pdf_base64, markdown: data.resume_markdown }));
        break;
        
      case 'resume_docx_update':
        setResumeData(prev => ({ ...prev, docx: data.docx_base64 }));
        break;
        
      case 'error':
        setStatus(prev => ({ ...prev, error: data.message, generating: false }));
        break;
    }
  };

  // Send message
  const sendMessage = async (message) => {
    if (!sessionId) throw new Error('No active session');
    
    setMessages(prev => [...prev, {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString()
    }]);

    const response = await fetch(`${baseUrl}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ session_id: sessionId, message })
    });
    
    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
  };

  // Download files
  const downloadFile = (base64Data, filename, mimeType) => {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    const blob = new Blob([byteArray], { type: mimeType });
    
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadPdf = (filename = 'resume.pdf') => {
    if (!resumeData.pdf) throw new Error('No PDF available');
    downloadFile(resumeData.pdf, filename, 'application/pdf');
  };

  const downloadDocx = (filename = 'resume.docx') => {
    if (!resumeData.docx) throw new Error('No DOCX available');
    downloadFile(resumeData.docx, filename, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document');
  };

  // Initialize on mount
  useEffect(() => {
    initialize();
    return () => {
      if (wsRef.current) wsRef.current.close();
    };
  }, []);

  return {
    sessionId,
    messages,
    resumeData,
    status,
    sendMessage,
    downloadPdf,
    downloadDocx
  };
};
```

### Step 2: Create Resume Component
```jsx
// components/ResumeBuilder.jsx
import React, { useState } from 'react';
import { useResumeBuilder } from '../hooks/useResumeBuilder';

export const ResumeBuilder = () => {
  const [input, setInput] = useState('');
  const { messages, resumeData, status, sendMessage, downloadPdf, downloadDocx } = useResumeBuilder();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || !status.connected) return;
    
    try {
      await sendMessage(input);
      setInput('');
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      {/* Status Bar */}
      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px', padding: '10px', background: '#f5f5f5', borderRadius: '5px' }}>
        <span style={{ color: status.connected ? 'green' : 'red' }}>
          {status.connected ? '🟢 Connected' : '🔴 Disconnected'}
        </span>
        {status.generating && <span>🔄 Generating...</span>}
        {status.error && <span style={{ color: 'red' }}>❌ {status.error}</span>}
      </div>

      {/* Chat Messages */}
      <div style={{ border: '1px solid #ddd', borderRadius: '5px', padding: '15px', marginBottom: '20px', maxHeight: '400px', overflowY: 'auto' }}>
        {messages.length === 0 ? (
          <p style={{ color: '#666', textAlign: 'center' }}>👋 Hi! I'm your AI resume builder. Tell me about your experience to get started.</p>
        ) : (
          messages.map((msg, index) => (
            <div key={index} style={{ marginBottom: '15px', padding: '10px', borderRadius: '5px', background: msg.role === 'user' ? '#e3f2fd' : '#f3e5f5' }}>
              <strong style={{ color: msg.role === 'user' ? '#1976d2' : '#7b1fa2' }}>
                {msg.role === 'user' ? '👤 You' : '🤖 AI'}:
              </strong>
              <div style={{ marginTop: '5px' }}>{msg.content}</div>
            </div>
          ))
        )}
      </div>

      {/* Input Form */}
      <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Tell me about your work experience, skills, education..."
          disabled={!status.connected || status.generating}
          style={{ 
            flex: 1, 
            padding: '12px', 
            border: '1px solid #ddd', 
            borderRadius: '5px',
            fontSize: '14px'
          }}
        />
        <button 
          type="submit" 
          disabled={!status.connected || status.generating || !input.trim()}
          style={{ 
            padding: '12px 20px', 
            background: '#2196f3', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: status.connected && !status.generating && input.trim() ? 'pointer' : 'not-allowed',
            opacity: status.connected && !status.generating && input.trim() ? 1 : 0.6
          }}
        >
          Send
        </button>
      </form>

      {/* Resume Preview & Downloads */}
      {resumeData.markdown && (
        <div>
          <h3 style={{ marginBottom: '15px' }}>📄 Your Resume</h3>
          
          {/* Download Buttons */}
          <div style={{ display: 'flex', gap: '10px', marginBottom: '15px' }}>
            {resumeData.pdf && (
              <button 
                onClick={() => downloadPdf()}
                style={{ padding: '10px 20px', background: '#4caf50', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                📄 Download PDF
              </button>
            )}
            {resumeData.docx && (
              <button 
                onClick={() => downloadDocx()}
                style={{ padding: '10px 20px', background: '#2196f3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
              >
                📝 Download DOCX
              </button>
            )}
          </div>

          {/* Markdown Preview */}
          <div style={{ border: '1px solid #ddd', borderRadius: '5px', padding: '15px', background: '#f9f9f9', maxHeight: '300px', overflowY: 'auto' }}>
            <pre style={{ whiteSpace: 'pre-wrap', margin: 0, fontSize: '12px', lineHeight: '1.4' }}>
              {resumeData.markdown}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};
```

### Step 3: Use in Your App
```jsx
// App.jsx
import React from 'react';
import { ResumeBuilder } from './components/ResumeBuilder';

function App() {
  return (
    <div className="App">
      <h1 style={{ textAlign: 'center', marginBottom: '30px' }}>
        🚀 AI Resume Builder
      </h1>
      <ResumeBuilder />
    </div>
  );
}

export default App;
```

---

## 2. Quick Examples

### Example Conversation Flow:
```
User: "I'm a senior software engineer with 5 years experience"
AI: "Great! Can you tell me about your current or most recent position?"

User: "I work at Google as a Senior Software Engineer focusing on backend systems"
AI: "Excellent! What technologies do you work with? And can you share some key achievements?"

User: "I use Python, Go, and Kubernetes. I led a team of 8 engineers and improved system performance by 40%"
AI: "Perfect! I'm starting to build your resume. Can you tell me about your education?"

// Resume generation starts automatically when enough info is collected
```

### Quick Modifications:
```
User: "Add that I know React and Node.js"
// ✅ Quick modification - updates existing resume without full regeneration

User: "Remove the Google experience and add Microsoft instead"
// ✅ Targeted modification - efficient updates

User: "Make the summary more focused on leadership"
// ✅ Intelligent modification - preserves other content
```

---

## 3. Common Use Cases

### A. Basic Resume Building
```javascript
// Start with basic info
await sendMessage("I'm a full-stack developer with 3 years experience");

// Add work experience
await sendMessage("I currently work at Spotify as a Frontend Developer using React and TypeScript");

// Add skills
await sendMessage("I'm skilled in JavaScript, Python, React, Node.js, and AWS");

// Add education
await sendMessage("I have a Bachelor's degree in Computer Science from Stanford");
```

### B. Resume Modifications
```javascript
// Quick edits
await sendMessage("Change my current title to Senior Frontend Developer");
await sendMessage("Add Docker and Kubernetes to my skills");
await sendMessage("Update my years of experience to 4 years");
```

### C. Download Management
```javascript
// Download when ready
if (resumeData.pdf) {
  downloadPdf('john-smith-resume.pdf');
}

if (resumeData.docx) {
  downloadDocx('john-smith-resume.docx');
}
```

---

## 4. Error Handling

### Connection Issues
```javascript
const handleConnectionError = () => {
  if (!status.connected) {
    return (
      <div style={{ padding: '20px', background: '#ffebee', color: '#c62828', borderRadius: '5px' }}>
        ❌ Connection lost. Please refresh the page to reconnect.
      </div>
    );
  }
  return null;
};
```

### Message Failures
```javascript
const sendMessageWithRetry = async (message, retries = 3) => {
  try {
    await sendMessage(message);
  } catch (error) {
    if (retries > 0) {
      console.log(`Retrying... ${retries} attempts left`);
      setTimeout(() => sendMessageWithRetry(message, retries - 1), 2000);
    } else {
      alert('Failed to send message. Please try again.');
    }
  }
};
```

---

## 5. Advanced Features

### Session Persistence
```javascript
// Save session ID to localStorage
useEffect(() => {
  if (sessionId) {
    localStorage.setItem('resume_session_id', sessionId);
  }
}, [sessionId]);

// Restore session on page load
const storedSessionId = localStorage.getItem('resume_session_id');
if (storedSessionId) {
  // Use stored session ID for reconnection
}
```

### Real-time Preview
```javascript
// Show live updates as they come in
useEffect(() => {
  if (resumeData.markdown) {
    // Update preview immediately
    setPreviewContent(resumeData.markdown);
  }
}, [resumeData.markdown]);
```

### File Management
```javascript
// Generate multiple formats
const generateAllFormats = async () => {
  if (resumeData.markdown) {
    try {
      const response = await fetch('/generate-docx', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          session_id: sessionId,
          markdown: resumeData.markdown
        })
      });
      const data = await response.json();
      // DOCX will be sent via WebSocket
    } catch (error) {
      console.error('Failed to generate DOCX:', error);
    }
  }
};
```

---

## 6. Styling & UI Tips

### Loading States
```jsx
{status.generating && (
  <div style={{ 
    display: 'flex', 
    alignItems: 'center', 
    gap: '10px', 
    padding: '10px',
    background: '#e3f2fd',
    borderRadius: '5px'
  }}>
    <div className="spinner">🔄</div>
    <span>Generating your resume...</span>
  </div>
)}
```

### Message Animations
```css
.message {
  animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
```

### Responsive Design
```jsx
<div style={{ 
  maxWidth: '100%', 
  padding: window.innerWidth > 768 ? '20px' : '10px',
  margin: '0 auto'
}}>
```

---

## 7. Environment Configuration

### Development
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

### Production
```javascript
const API_BASE_URL = 'https://your-resume-api.com';
```

### Environment Variables
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

---

That's it! 🎉 Copy these components into your React app and you'll have a fully functional AI resume builder with real-time updates, file downloads, and intelligent conversation handling.