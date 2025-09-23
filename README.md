# AI Resume Generator

A production-ready FastAPI application that generates and live-edits resumes using AI agents. Features real-time chat interface with WebSocket updates and professional resume generation.

## 🚀 Features

- **Dual AI Agent System**: 
  - Data Gathering Agent: Conducts intelligent conversations to collect user information
  - Resume Generator Agent: Creates professional, ATS-optimized resumes in markdown format
  
- **Real-time Interface**: WebSocket-powered live updates as resume is generated
- **Session Management**: Redis-backed session storage with fallback to in-memory
- **Production Ready**: Docker containerization, nginx reverse proxy, rate limiting
- **Responsive Design**: Clean, mobile-friendly web interface

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Chat     │◄──►│  FastAPI Server │◄──►│   AI Agents     │
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

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review logs with `docker-compose logs -f`