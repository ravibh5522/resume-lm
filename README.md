# 🚀 AI Resume Generator

An intelligent resume generation platform with real-time chat interface, file processing capabilities, and multiple output formats. Built with FastAPI, WebSocket real-time updates, and AI-powered content generation.

## ✨ Features

- **🤖 AI-Powered Resume Generation**: Intelligent content creation and optimization
- **💬 Real-time Chat Interface**: Interactive conversation for resume building
- **📎 File Upload Support**: Process images and PDFs for resume enhancement
- **📄 Multiple Output Formats**: Generate PDF and DOCX resumes
- **⚡ Live Updates**: WebSocket-powered real-time status updates
- **🎛️ Auto-fit Technology**: Intelligent content fitting and font optimization
- **🔄 Resume Modification**: Quick edits without full regeneration

## 🏗️ Architecture

```
├── FastAPI Backend (main.py)
├── WebSocket Manager (real-time updates)
├── AI Agent Orchestrator (intelligent processing)
├── File Processor (image/PDF handling)
├── Resume Generators (PDF/DOCX)
├── Session Manager (state persistence)
└── Web UI (HTML/CSS/JavaScript)
```

## 📚 API Documentation

### 🔗 Base URL
```
http://localhost:8000
```

### 📋 Endpoints Overview

| Method | Endpoint | Description | File Upload |
|--------|----------|-------------|-------------|
| `GET` | `/` | Web UI Interface | ✅ |
| `POST` | `/create-session` | Create new chat session | ❌ |
| `POST` | `/chat` | Send message with attachments | ✅ |
| `POST` | `/generate-docx` | Generate DOCX from markdown | ❌ |
| `GET` | `/session/{session_id}` | Get session data | ❌ |
| `GET` | `/resume/{session_id}` | Get resume markdown | ❌ |
| `WS` | `/ws/{session_id}` | WebSocket connection | ❌ |
| `GET` | `/health` | Health check | ❌ |

---

## 🔥 Detailed API Reference

### 1. 🌐 Web Interface
```http
GET /
```

**Description**: Serves the interactive web UI with file upload capabilities

**Features**:
- Real-time chat interface
- Drag & drop file upload
- PDF/DOCX preview and download
- WebSocket live updates

**Usage Example**:
```bash
curl http://localhost:8000
# Or open in browser: http://localhost:8000
```

---

### 2. 🆕 Create Session
```http
POST /create-session
```

**Description**: Creates a new chat session for resume generation

**Request Body**: None

**Response**:
```json
{
  "session_id": "uuid-string"
}
```

**JavaScript Example**:
```javascript
fetch('/create-session', { 
    method: 'POST' 
})
.then(response => response.json())
.then(data => {
    console.log('Session created:', data.session_id);
});
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/create-session
```

---

### 3. � Chat with File Upload
```http
POST /chat
```

**Description**: Send messages with optional file attachments (images/PDFs)

**Request Body**:
```json
{
  "message": "Please review my resume and suggest improvements",
  "session_id": "your-session-id",
  "attachments": [
    {
      "filename": "resume.pdf",
      "file_type": "pdf",
      "content": "base64-encoded-content",
      "mime_type": "application/pdf",
      "extracted_text": ""
    }
  ]
}
```

**Response**:
```json
{
  "message": "I've analyzed your resume. Here are my suggestions...",
  "session_id": "your-session-id",
  "timestamp": "2025-09-29T10:30:00"
}
```

**JavaScript File Upload Example**:
```javascript
async function sendMessageWithFiles() {
    const fileInput = document.getElementById('fileInput');
    const files = fileInput.files;
    const attachments = [];
    
    // Process files
    for (const file of files) {
        const base64 = await readFileAsBase64(file);
        attachments.push({
            filename: file.name,
            file_type: file.type.startsWith('image/') ? 'image' : 'pdf',
            content: base64.split(',')[1], // Remove data:type;base64, prefix
            mime_type: file.type,
            extracted_text: ''
        });
    }
    
    // Send request
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: 'Analyze my resume',
            session_id: sessionId,
            attachments: attachments
        })
    });
    
    const result = await response.json();
    console.log('AI Response:', result.message);
}

function readFileAsBase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a software engineer resume",
    "session_id": "your-session-id",
    "attachments": []
  }'
```

**Supported File Types**:
- **Images**: JPEG, PNG, GIF, BMP, WebP, TIFF
- **Documents**: PDF (with text extraction)

---

### 4. 📝 Generate DOCX
```http
POST /generate-docx
```

**Description**: Convert resume markdown to DOCX format

**Request Body**:
```json
{
  "markdown": "# John Doe\n\n## Experience\n...",
  "session_id": "your-session-id"
}
```

**Response**:
```json
{
  "docx_base64": "base64-encoded-docx-content",
  "session_id": "your-session-id",
  "success": true,
  "error": null
}
```

**JavaScript Example**:
```javascript
async function generateDocx() {
    const response = await fetch('/generate-docx', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            markdown: resumeMarkdown,
            session_id: sessionId
        })
    });
    
    const result = await response.json();
    if (result.success) {
        // Download the DOCX file
        const link = document.createElement('a');
        link.href = `data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,${result.docx_base64}`;
        link.download = 'resume.docx';
        link.click();
    }
}
```

---

### 5. 📊 Get Session Data
```http
GET /session/{session_id}
```

**Description**: Retrieve complete session information

**Response**:
```json
{
  "session_id": "uuid-string",
  "user_data": {
    "profile": { "name": "John Doe", "email": "john@example.com" },
    "experience": [...],
    "education": [...]
  },
  "chat_history": [...],
  "resume_markdown": "# Resume content...",
  "last_updated": "2025-09-29T10:30:00",
  "status": "active"
}
```

**JavaScript Example**:
```javascript
async function getSessionData(sessionId) {
    const response = await fetch(`/session/${sessionId}`);
    const sessionData = await response.json();
    console.log('Session data:', sessionData);
}
```

---

### 6. 📄 Get Resume
```http
GET /resume/{session_id}
```

**Description**: Get only the resume markdown content

**Response**:
```json
{
  "session_id": "uuid-string",
  "resume_markdown": "# John Doe\n\n## Professional Summary\n...",
  "last_updated": "2025-09-29T10:30:00"
}
```

---

### 7. 🔌 WebSocket Connection
```ws
WS /ws/{session_id}
```

**Description**: Real-time updates for resume generation and chat responses

**Connection Example**:
```javascript
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    
    switch(data.type) {
        case 'chat_response':
            displayMessage(data.message, 'assistant');
            break;
        case 'resume_pdf_update':
            updatePDFPreview(data.pdf_base64);
            break;
        case 'resume_docx_update':
            updateDocxPreview(data.docx_base64);
            break;
        case 'status_update':
            showStatus(data.message);
            break;
        case 'error':
            showError(data.message);
            break;
    }
};
```

**WebSocket Message Types**:
- `chat_response`: AI chat responses
- `resume_pdf_update`: PDF generation complete
- `resume_docx_update`: DOCX generation complete
- `status_update`: Progress notifications
- `error`: Error messages

---

### 8. ❤️ Health Check
```http
GET /health
```

**Description**: Service health status

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2025-09-29T10:30:00"
}
```

---

## 🚀 Quick Start Guide

### 1. **Start the Server**
```bash
cd /path/to/resume-lm
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### 2. **Open Web Interface**
```bash
# Open in browser
http://localhost:8000
```

### 3. **Basic Chat Flow**
```javascript
// 1. Create session
const sessionResponse = await fetch('/create-session', { method: 'POST' });
const { session_id } = await sessionResponse.json();

// 2. Connect WebSocket
const ws = new WebSocket(`ws://localhost:8000/ws/${session_id}`);

// 3. Send chat message
await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: 'I am a software engineer with 5 years of experience...',
        session_id: session_id,
        attachments: []
    })
});

// 4. Receive real-time updates via WebSocket
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};
```

---

## 📁 File Upload Implementation

### Frontend Implementation
```html
<!-- File Upload UI -->
<div class="file-upload-section">
    <input type="file" id="fileInput" multiple accept="image/*,.pdf">
    <label for="fileInput" class="file-button">📎 Add Files</label>
    <div class="file-list" id="fileList"></div>
</div>
```

```javascript
// Drag and Drop Support
function setupDragAndDrop() {
    const chatContainer = document.querySelector('.chat-container');
    
    chatContainer.addEventListener('dragover', (e) => {
        e.preventDefault();
        chatContainer.style.backgroundColor = '#f0f8ff';
    });
    
    chatContainer.addEventListener('drop', (e) => {
        e.preventDefault();
        const files = Array.from(e.dataTransfer.files);
        handleFiles(files);
    });
}

async function handleFiles(files) {
    for (const file of files) {
        if (file.type.startsWith('image/') || file.type === 'application/pdf') {
            selectedFiles.push(file);
            updateFileList();
        }
    }
}
```

---

## 🔧 Configuration

### Environment Variables
```bash
# .env file
ENVIRONMENT=development  # or production
HOST=0.0.0.0
PORT=8000
OPENAI_API_KEY=your-api-key
```

### Supported File Types
```python
# Images
SUPPORTED_IMAGES = {
    'image/jpeg', 'image/jpg', 'image/png', 'image/gif',
    'image/bmp', 'image/webp', 'image/tiff'
}

# Documents
SUPPORTED_DOCS = {'application/pdf'}
```

---

## 🏃‍♂️ Example Workflows

### 1. **Resume Creation from Scratch**
```javascript
// Start new session
const session = await createSession();

// Send work experience
await sendMessage("I'm a senior software engineer at Google with 6 years experience in Python, React, and cloud architecture.");

// Upload existing resume for reference
await sendMessageWithFile("Please improve this resume", resumePDF);

// Get generated resume
const resume = await getResume(session.session_id);
```

### 2. **Resume Enhancement with File Upload**
```javascript
// Upload current resume
const fileAttachment = {
    filename: "current_resume.pdf",
    file_type: "pdf",
    content: base64PDFContent,
    mime_type: "application/pdf"
};

await fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: "Please modernize this resume and add relevant keywords for tech roles",
        session_id: sessionId,
        attachments: [fileAttachment]
    })
});
```

### 3. **Real-time Resume Building**
```javascript
// Connect WebSocket for live updates
const ws = new WebSocket(`ws://localhost:8000/ws/${sessionId}`);

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.type === 'resume_pdf_update') {
        // Show PDF preview immediately
        document.getElementById('pdfPreview').src = 
            `data:application/pdf;base64,${data.pdf_base64}`;
    }
};

// Send iterative improvements
await sendMessage("Add more technical leadership experience");
await sendMessage("Make the summary more concise");
await sendMessage("Add relevant certifications section");
```

---

## 🐛 Error Handling

### Common Error Responses
```json
// File too large
{
  "detail": "File size exceeds maximum limit",
  "status_code": 413
}

// Unsupported file type
{
  "detail": "Unsupported file type: application/vnd.ms-excel",
  "status_code": 400
}

// Session not found
{
  "detail": "Session not found",
  "status_code": 404
}

// Processing error
{
  "detail": "Failed to process PDF: corrupted file",
  "status_code": 422
}
```

### JavaScript Error Handling
```javascript
try {
    const response = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(chatRequest)
    });
    
    if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const result = await response.json();
    return result;
    
} catch (error) {
    console.error('Chat request failed:', error);
    showErrorMessage('Failed to send message. Please try again.');
}
```

---

## 📈 Performance & Limits

### File Upload Limits
- **Maximum file size**: 10MB per file
- **Maximum files per message**: 5 files
- **Supported concurrent sessions**: 100
- **WebSocket connection timeout**: 1 hour

### Rate Limiting
- **Chat requests**: 30 per minute per session
- **File uploads**: 10 per minute per session
- **DOCX generation**: 5 per minute per session

---

## 🛠️ Development

### Local Development Setup
```bash
# Clone repository
git clone <repo-url>
cd resume-lm

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run in development mode
ENVIRONMENT=development python main.py
```

### Testing File Upload
```bash
# Test PDF upload
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze this resume",
    "session_id": "test-session",
    "attachments": [{
      "filename": "test.pdf",
      "file_type": "pdf", 
      "content": "'$(base64 -w 0 test.pdf)'",
      "mime_type": "application/pdf"
    }]
  }'
```
│   Interface     │    │   + WebSocket   │    │   (OpenAI)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                               │
                               ▼
                       ┌─────────────────┐
                       │ Session Manager │
                       │   (Redis/Mem)   │
                       └─────────────────┘
```

## 📋 Prerequisites

- Python 3.11+
- Docker & Docker Compose (for containerized deployment)
- Redis (optional, falls back to in-memory storage)
- OpenAI API access via LiteLLM proxy

## 🔧 Installation & Setup

### 1. Clone and Setup Environment

```bash
git clone <repository>
cd resume-lm
```

### 2. Create Environment Configuration

Create a `.env` file with your configuration:

```env
OPENAI_API_KEY=sk-CxXh7gykTHvf9Vvi3x9Ehg
OPENAI_BASE_URL=https://proxyllm.ximplify.id/
OPENAI_MODEL=azure/gpt-4.1
REDIS_URL=redis://localhost:6379
SESSION_SECRET_KEY=your-secret-key-change-this-in-production
ENVIRONMENT=development
```

### 3. Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Test the setup
python test_setup.py

# Run development server
python main.py
```

### 4. Production Deployment

```bash
# Quick deployment with Docker
./deploy.sh

# Or manually
docker-compose up -d
```

## 🎯 Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Start chatting with the AI about your work experience
3. Watch your resume generate in real-time in the preview panel
4. The AI will guide you through providing all necessary information

### API Endpoints

#### Create Session
```bash
POST /create-session
Response: {"session_id": "uuid"}
```

#### Chat with AI
```bash
POST /chat
{
  "message": "I'm a software engineer with 5 years experience",
  "session_id": "session-uuid"
}
```

#### Get Resume
```bash
GET /resume/{session_id}
Response: {
  "session_id": "uuid",
  "resume_markdown": "# John Doe\n...",
  "last_updated": "2025-09-23T..."
}
```

#### WebSocket Connection
```javascript
ws://localhost:8000/ws/{session_id}
```

## 🤖 AI Agent Workflow

### 1. Data Gathering Agent
- Conducts natural conversation to collect user information
- Asks targeted questions about experience, education, skills
- Validates completeness before proceeding to generation
- Signals when ready with `READY_TO_GENERATE_RESUME:` marker

### 2. Resume Generator Agent  
- Transforms structured data into professional markdown resume
- Optimizes for ATS compatibility
- Emphasizes achievements and quantifiable results
- Uses modern resume formatting and best practices

### Example Conversation Flow:
```
User: "Hi, I need help creating a resume"
AI: "I'd be happy to help! Let's start with your name and contact information..."

User: "I'm John Doe, email john@example.com..."
AI: "Great! Now tell me about your work experience..."

[After sufficient information]
AI: "Perfect! I have all the information needed. Generating your resume now..."
→ Resume appears in real-time via WebSocket
```

## 🔒 Production Considerations

### Security Features
- Rate limiting (10 req/s for chat, 30 req/s for API)
- Security headers (XSS protection, content type sniffing prevention)
- CORS configuration
- Input validation with Pydantic models

### Monitoring & Logging
- Health check endpoint `/health`
- Structured logging
- Docker health checks
- Nginx access logs

### Scalability
- Redis session storage for horizontal scaling
- Async processing for resume generation
- WebSocket connection management
- Resource limits in Docker containers

### Configuration Management
- Environment-based configuration
- Docker secrets support
- SSL/TLS termination at nginx level

## 🛠️ Development

### Project Structure
```
resume-lm/
├── agents.py           # AI agent implementations
├── main.py            # FastAPI application
├── models.py          # Pydantic data models
├── session_manager.py # Session storage logic
├── resume_generator.py # Resume generation service
├── requirements.txt   # Python dependencies
├── Dockerfile         # Container definition
├── docker-compose.yml # Multi-service setup
├── nginx.conf         # Reverse proxy config
└── test_setup.py      # Test script
```

### Running Tests
```bash
# Test core functionality
python test_setup.py

# Run with coverage (if pytest installed)
pytest --cov=. tests/
```

### Adding New Features

1. **Extend Models**: Update `models.py` for new data structures
2. **Enhance Agents**: Modify prompts and logic in `agents.py`
3. **Add Endpoints**: Extend FastAPI routes in `main.py`
4. **Update Frontend**: Modify HTML/JavaScript in main route

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   ```bash
   # Check API key and base URL
   curl -H "Authorization: Bearer $OPENAI_API_KEY" $OPENAI_BASE_URL/models
   ```

2. **Redis Connection Issues**
   ```bash
   # Check Redis connectivity
   redis-cli ping
   # Falls back to in-memory storage if Redis unavailable
   ```

3. **WebSocket Connection Problems**
   ```bash
   # Check if port 8000 is accessible
   curl http://localhost:8000/health
   ```

4. **Docker Issues**
   ```bash
   # Check container logs
   docker-compose logs -f app
   
   # Rebuild containers
   docker-compose down && docker-compose up --build -d
   ```

### Debug Mode
Set `ENVIRONMENT=development` in `.env` for verbose logging.

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

---

## 📞 Support

For issues, feature requests, or questions:
- **GitHub Issues**: [Create an issue](https://github.com/ravibh5522/resume-lm/issues)
- **Documentation**: Check inline code comments and API documentation
- **WebSocket Debug**: Use browser developer tools Network tab
- **File Upload Issues**: Verify file types and sizes meet requirements

---

**Built with ❤️ using FastAPI, WebSocket, and AI technology**