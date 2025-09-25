import asyncio
import json
from datetime import datetime
from typing import Dict, Set
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Import our modules
from models import (
    ChatRequest, ChatResponse, ChatMessage, ChatRole, 
    ResumeData, SessionData, ResumeUpdateEvent,
    DocxGenerationRequest, DocxResponse
)
from session_manager import SessionManager
from agents import AIAgentOrchestrator
from resume_generator import ResumeGenerationService
from pdf_generator_optimized import OptimizedPDFGenerator
from pdf_generator_enhanced import EnhancedPdfGenerator
from ultimate_parser import UltimatePdfGenerator
from compact_parser import CompactPdfGenerator
from auto_fit_generator import AutoFitPdfGenerator
from docx_generator import ProfessionalDocxGenerator
from docx_generator_enhanced import EnhancedDocxGenerator
from compact_docx_generator import CompactDocxGenerator
from auto_fit_docx_generator import AutoFitDocxGenerator
from unified_parser import UnifiedResumeParser
from resume_modifier import ResumeModifier

load_dotenv()

# Get environment variables
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

print(f"🚀 Starting AI Resume Generator in {ENVIRONMENT} mode...")
print(f"📍 Server will run on {HOST}:{PORT}")

# Initialize FastAPI app
app = FastAPI(
    title="AI Resume Generator",
    description="Generate and live edit resumes with AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with AUTO-FIT generators - automatic font scaling for single-page layout
session_manager = SessionManager()
ai_orchestrator = AIAgentOrchestrator()
resume_service = ResumeGenerationService(session_manager)
pdf_generator = AutoFitPdfGenerator()        # AUTO-FIT PDF - dynamic font scaling for single-page
docx_generator = AutoFitDocxGenerator()      # AUTO-FIT DOCX - adaptive sizing for Word documents
unified_parser = UnifiedResumeParser()      # For format conversion
resume_modifier = ResumeModifier()

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        self.active_connections[session_id] = websocket
    
    def disconnect(self, session_id: str):
        if session_id in self.active_connections:
            del self.active_connections[session_id]
    
    async def send_personal_message(self, message: dict, session_id: str):
        if session_id in self.active_connections:
            try:
                await self.active_connections[session_id].send_text(json.dumps(message))
            except Exception as e:
                print(f"Error sending message to {session_id}: {e}")
                self.disconnect(session_id)

manager = ConnectionManager()

# Routes
@app.get("/")
async def root():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Resume Builder</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f5f5f5; height: 100vh; overflow: hidden; }
            .container { height: 100vh; display: grid; grid-template-columns: 1fr 1fr; gap: 0; }
            .panel { background: white; padding: 20px; display: flex; flex-direction: column; }
            .panel:first-child { border-right: 1px solid #ddd; }
            .chat-container { flex: 1; display: flex; flex-direction: column; height: calc(100vh - 40px); }
            .chat-messages { 
                flex: 1; 
                overflow-y: auto; 
                border: 1px solid #ddd; 
                padding: 10px; 
                margin-bottom: 10px; 
                border-radius: 4px; 
                scroll-behavior: smooth;
                max-height: calc(100vh - 120px);
                position: relative;
            }
            .chat-messages::-webkit-scrollbar {
                width: 8px;
            }
            .chat-messages::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            .chat-messages::-webkit-scrollbar-thumb {
                background: #c1c1c1;
                border-radius: 4px;
            }
            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: #a8a8a8;
            }
            .message { 
                margin: 10px 0; 
                padding: 10px; 
                border-radius: 5px; 
                word-wrap: break-word; 
                overflow-wrap: break-word;
                max-width: 100%;
                line-height: 1.4;
            }
            .user-message { background: #e3f2fd; margin-left: 20px; }
            .assistant-message { background: #f3e5f5; margin-right: 20px; }
            .chat-input { 
                display: flex; 
                gap: 10px; 
                padding: 10px 0; 
                position: sticky; 
                bottom: 0; 
                background: white; 
                border-top: 1px solid #eee; 
                margin-top: auto;
            }
            .chat-input input { 
                flex: 1; 
                padding: 12px; 
                border: 1px solid #ddd; 
                border-radius: 4px; 
                font-size: 14px; 
                resize: none;
                min-height: 44px;
                max-height: 120px;
                overflow-y: auto;
            }
            .chat-input button { 
                padding: 12px 24px; 
                background: #2196f3; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                font-size: 14px; 
                align-self: flex-end;
            }
            .chat-input button:hover { background: #1976d2; }
            
            /* Format Selection Tabs */
            .format-tabs {
                display: flex;
                margin-bottom: 15px;
                border-bottom: 2px solid #f0f0f0;
            }
            .format-tab {
                flex: 1;
                padding: 12px 20px;
                background: #f8f9fa;
                border: none;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                color: #666;
                transition: all 0.2s;
                border-radius: 8px 8px 0 0;
                margin-right: 2px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 8px;
            }
            .format-tab:last-child { margin-right: 0; }
            .format-tab.active {
                background: #2196f3;
                color: white;
                border-bottom: 2px solid #2196f3;
            }
            .format-tab:hover:not(.active) {
                background: #e3f2fd;
                color: #1976d2;
            }
            
            .resume-preview { 
                flex: 1; 
                overflow-y: auto; 
                border: 1px solid #ddd; 
                background: #fafafa; 
                border-radius: 4px; 
                display: block;
            }
            .resume-preview.hidden { display: none; }
            
            .status { padding: 8px 12px; background: #e8f5e8; border-radius: 4px; margin-bottom: 10px; font-size: 13px; }
            h2 { color: #333; margin-bottom: 15px; font-size: 18px; border-bottom: 2px solid #2196f3; padding-bottom: 8px; }
            
            /* Download Button */
            .download-btn {
                position: absolute;
                top: 10px;
                right: 10px;
                background: #4caf50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                font-size: 12px;
                z-index: 1000;
                display: none;
            }
            .download-btn:hover { background: #45a049; }
            .download-btn.show { display: block; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="panel">
                <h2>💬 Chat with AI</h2>
                <div class="status" id="status">Connecting...</div>
                <div class="chat-container">
                    <div class="chat-messages" id="chatMessages"></div>
                    <div class="chat-input">
                        <input type="text" id="messageInput" placeholder="Tell me about your work experience..." onkeypress="handleKeyPress(event)">
                        <button onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <h2>📄 Resume Preview</h2>
                
                <!-- Format Selection Tabs -->
                <div class="format-tabs">
                    <button class="format-tab active" onclick="switchFormat('pdf')" id="pdfTab">
                        📄 PDF Preview
                    </button>
                    <button class="format-tab" onclick="switchFormat('docx')" id="docxTab">
                        📝 Word Preview
                    </button>
                </div>
                
                <!-- Download Button -->
                <button class="download-btn" id="downloadBtn" onclick="downloadResume()">📥 Download</button>
                
                <!-- PDF Preview -->
                <div class="resume-preview" id="pdfPreview">
                    <div style="text-align: center; padding: 40px; color: #666;">
                        <h3 style="margin-bottom: 20px;">� Professional PDF Resume</h3>
                        <p><em>Your A4 PDF resume will appear here as you chat with the AI...</em></p>
                        <p style="margin-top: 20px; font-size: 14px;">✨ Modern styling • 📏 A4 format • 🖨️ Print-ready</p>
                    </div>
                </div>
                
                <!-- DOCX Preview -->
                <div class="resume-preview hidden" id="docxPreview">
                    <div style="text-align: center; padding: 40px; color: #666;">
                        <h3 style="margin-bottom: 20px;">📝 Professional Word Document</h3>
                        <p><em>Your Word resume preview will appear here...</em></p>
                        <p style="margin-top: 20px; font-size: 14px;">💼 Professional styling • 📝 Editable format • 🔄 Live updates</p>
                    </div>
                </div>
            </div>
        </div>

        <script>
            let ws;
            let sessionId;
            let currentFormat = 'pdf';
            let resumeData = {
                pdf: null,
                docx: null,
                markdown: null
            };

            // Initialize WebSocket connection
            function initWebSocket() {
                // First create a session
                fetch('/create-session', { method: 'POST' })
                    .then(response => response.json())
                    .then(data => {
                        sessionId = data.session_id;
                        document.getElementById('status').textContent = `Session: ${sessionId}`;
                        
                        // Connect WebSocket - dynamically detect host and protocol
                        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                        const host = window.location.host;
                        const wsUrl = `${protocol}//${host}/ws/${sessionId}`;
                        console.log(`Connecting to WebSocket: ${wsUrl}`);
                        ws = new WebSocket(wsUrl);
                        
                        ws.onopen = function(event) {
                            document.getElementById('status').textContent = `Connected - Session: ${sessionId}`;
                            // Focus on input when connected
                            document.getElementById('messageInput').focus();
                        };
                        
                        ws.onmessage = function(event) {
                            const data = JSON.parse(event.data);
                            if (data.type === 'resume_pdf_update') {
                                updateResumePDFPreview(data.pdf_base64);
                                if (data.resume_markdown) {
                                    resumeData.markdown = data.resume_markdown;
                                }
                            } else if (data.type === 'resume_docx_update') {
                                updateResumeDocxPreview(data.docx_base64);
                            } else if (data.type === 'resume_update') {
                                updateResumePreview(data.resume_markdown);
                            } else if (data.type === 'chat_response') {
                                addMessage(data.message, 'assistant');
                            } else if (data.type === 'status_update') {
                                addMessage(data.message, 'status');
                            }
                        };
                        
                        ws.onclose = function(event) {
                            document.getElementById('status').textContent = 'Disconnected. Refresh to reconnect.';
                        };
                        
                        ws.onerror = function(error) {
                            document.getElementById('status').textContent = 'Connection error. Please refresh.';
                        };
                    });
            }

            // Format switching functionality
            function switchFormat(format) {
                currentFormat = format;
                
                // Update tab styles
                document.querySelectorAll('.format-tab').forEach(tab => {
                    tab.classList.remove('active');
                });
                document.getElementById(format + 'Tab').classList.add('active');
                
                // Show/hide previews
                document.getElementById('pdfPreview').classList.toggle('hidden', format !== 'pdf');
                document.getElementById('docxPreview').classList.toggle('hidden', format !== 'docx');
                
                // Generate DOCX if switching to DOCX and we have markdown data
                if (format === 'docx' && resumeData.markdown && !resumeData.docx) {
                    generateDocxFromMarkdown();
                }
                
                // Update download button
                updateDownloadButton();
            }

            // Generate DOCX from current markdown
            function generateDocxFromMarkdown() {
                if (!resumeData.markdown) return;
                
                addMessage('🔄 Converting to Word format...', 'status');
                
                fetch('/generate-docx', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ 
                        markdown: resumeData.markdown,
                        session_id: sessionId 
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.docx_base64) {
                        updateResumeDocxPreview(data.docx_base64);
                        addMessage('✅ Word format ready!', 'status');
                    } else {
                        addMessage('❌ Error generating Word format', 'status');
                    }
                })
                .catch(error => {
                    console.error('Error generating DOCX:', error);
                    addMessage('❌ Error generating Word format', 'status');
                });
            }

            // Download current format
            function downloadResume() {
                if (currentFormat === 'pdf' && resumeData.pdf) {
                    const link = document.createElement('a');
                    link.href = `data:application/pdf;base64,${resumeData.pdf}`;
                    link.download = 'resume.pdf';
                    link.click();
                } else if (currentFormat === 'docx' && resumeData.docx) {
                    const link = document.createElement('a');
                    link.href = `data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;base64,${resumeData.docx}`;
                    link.download = 'resume.docx';
                    link.click();
                }
            }

            // Update download button visibility and text
            function updateDownloadButton() {
                const downloadBtn = document.getElementById('downloadBtn');
                const hasData = (currentFormat === 'pdf' && resumeData.pdf) || 
                               (currentFormat === 'docx' && resumeData.docx);
                
                downloadBtn.classList.toggle('show', hasData);
                downloadBtn.textContent = currentFormat === 'pdf' ? '📄 Download PDF' : '📝 Download Word';
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter' && !event.shiftKey) {
                    event.preventDefault();
                    sendMessage();
                }
            }

            function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (message && ws && ws.readyState === WebSocket.OPEN) {
                    addMessage(message, 'user');
                    
                    fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message, session_id: sessionId })
                    })
                    .then(response => response.json())
                    .then(data => {
                        // Response will come via WebSocket
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        addMessage('Error sending message. Please try again.', 'assistant');
                    });
                    
                    input.value = '';
                    input.focus(); // Keep focus on input after sending
                }
            }

            function addMessage(message, role) {
                const messagesDiv = document.getElementById('chatMessages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${role}-message`;
                
                if (role === 'status') {
                    messageDiv.innerHTML = `<strong>Status:</strong> ${message}`;
                    messageDiv.style.backgroundColor = '#e3f2fd';
                    messageDiv.style.color = '#1565c0';
                    messageDiv.style.fontStyle = 'italic';
                } else {
                    messageDiv.innerHTML = `<strong>${role === 'user' ? 'You' : 'AI'}:</strong> ${message}`;
                }
                
                messagesDiv.appendChild(messageDiv);
                
                // Enhanced auto-scrolling with smooth behavior
                setTimeout(() => {
                    messagesDiv.scrollTo({
                        top: messagesDiv.scrollHeight,
                        behavior: 'smooth'
                    });
                }, 50);
            }

            function updateResumePDFPreview(pdfBase64) {
                resumeData.pdf = pdfBase64;
                
                const preview = document.getElementById('pdfPreview');
                
                if (pdfBase64) {
                    // Create PDF viewer with embedded PDF
                    preview.innerHTML = `
                        <div style="border: 1px solid #ddd; border-radius: 5px; overflow: hidden; height: calc(100vh - 200px); box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                            <embed src="data:application/pdf;base64,${pdfBase64}" 
                                   type="application/pdf" 
                                   width="100%" 
                                   height="100%" 
                                   style="border: none;">
                        </div>
                        <p style="text-align: center; color: #666; margin-top: 10px; font-size: 12px;">
                            📏 Professional A4 format • 🖨️ Print-ready • 🔒 Consistent across all devices
                        </p>
                    `;
                } else {
                    preview.innerHTML = '<p style="color: red; text-align: center; padding: 40px;">❌ Error loading PDF preview</p>';
                }
                
                updateDownloadButton();
            }

            function updateResumeDocxPreview(docxBase64) {
                resumeData.docx = docxBase64;
                
                const preview = document.getElementById('docxPreview');
                
                if (docxBase64) {
                    // For DOCX, we'll show a preview message and download option since browsers can't embed DOCX
                    preview.innerHTML = `
                        <div style="text-align: center; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white; margin: 20px;">
                            <h3 style="margin-bottom: 20px; color: white;">📝 Microsoft Word Document Ready!</h3>
                            <p style="margin-bottom: 25px; opacity: 0.9;">Your professional resume has been generated in Word format.</p>
                            <button onclick="downloadResume()" style="background: #4CAF50; color: white; border: none; padding: 15px 30px; border-radius: 25px; font-size: 16px; cursor: pointer; box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: all 0.3s;">
                                📥 Download Word Document
                            </button>
                            <div style="margin-top: 25px; padding: 20px; background: rgba(255,255,255,0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.2);">
                                <h4 style="margin-bottom: 15px; color: white;">📋 Word Document Features:</h4>
                                <ul style="text-align: left; display: inline-block; opacity: 0.9;">
                                    <li>✏️ Fully editable in Microsoft Word</li>
                                    <li>🎨 Professional formatting preserved</li>
                                    <li>📱 Compatible with Word Online & mobile</li>
                                    <li>🔄 Easy to customize further</li>
                                    <li>📧 Perfect for email attachments</li>
                                </ul>
                            </div>
                        </div>
                        <p style="text-align: center; color: #666; margin-top: 15px; font-size: 12px;">
                            � Professional Word format • ✏️ Fully editable • � ATS-compatible
                        </p>
                    `;
                } else {
                    preview.innerHTML = '<p style="color: red; text-align: center; padding: 40px;">❌ Error loading Word preview</p>';
                }
                
                updateDownloadButton();
            }

            function updateResumePreview(markdown) {
                resumeData.markdown = markdown;
                
                // If we're currently viewing PDF, update that
                if (currentFormat === 'pdf') {
                    const preview = document.getElementById('pdfPreview');
                    
                    // Simple but working markdown to HTML conversion (fallback)
                    let html = markdown
                        // Headers
                        .replace(/^# (.*)$/gm, '<h1 style="color: #1565c0; text-align: center; border-bottom: 3px solid #4caf50; padding-bottom: 10px; margin-bottom: 20px;">$1</h1>')
                        .replace(/^## (.*)$/gm, '<h2 style="color: #1976d2; margin-top: 25px; margin-bottom: 15px; border-bottom: 2px solid #81c784; padding-bottom: 5px;">$1</h2>')
                        .replace(/^### (.*)$/gm, '<h3 style="color: #424242; margin-top: 20px; margin-bottom: 10px;">$1</h3>')
                        
                        // Horizontal rules
                        .replace(/^---$/gm, '<hr style="border: none; height: 2px; background: linear-gradient(90deg, #4caf50, #2196f3); margin: 20px 0; border-radius: 1px;">')
                        
                        // Convert line breaks to HTML
                        .replace(/\\n/g, '<br>');
                    
                    // Apply modern container styling
                    preview.innerHTML = 
                        '<div style="font-family: \\'Segoe UI\\', \\'Roboto\\', \\'Helvetica Neue\\', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 900px; margin: 0 auto; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); border: 1px solid #e1e5e9;">' +
                        '<div style="background: white; padding: 25px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.08);">' +
                        html +
                        '</div></div>';
                }
                
                // If we have DOCX preview active, clear it so it regenerates
                if (currentFormat === 'docx') {
                    resumeData.docx = null;
                    generateDocxFromMarkdown();
                }
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            // Initialize when page loads
            window.onload = initWebSocket;
        </script>
    </body>
    </html>
    """)

@app.post("/create-session")
async def create_session():
    """Create a new chat session"""
    session_id = session_manager.create_session()
    return {"session_id": session_id}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """Handle chat messages"""
    try:
        # Get session
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Add user message to session
        user_message = ChatMessage(role=ChatRole.USER, content=request.message)
        session_manager.add_chat_message(request.session_id, user_message)
        
        # CHECK FOR TARGETED MODIFICATIONS FIRST
        existing_resume = session.resume_markdown
        if existing_resume and resume_modifier.can_handle_modification(request.message, existing_resume):
            # Handle as targeted modification without full regeneration
            impact = resume_modifier.estimate_change_impact(request.message)
            
            # Apply targeted modification
            modified_resume = resume_modifier.apply_modification(request.message, existing_resume)
            
            # Update session with modified resume
            session_manager.update_resume_markdown(request.session_id, modified_resume)
            
            # Generate PDF from modified resume
            asyncio.create_task(apply_quick_modification(request.session_id, modified_resume, request.message, impact))
            
            # Send quick response
            response_text = f"✅ Applied your {impact} modification: '{request.message}'. Updating your resume now..."
            
            # Add AI response to session
            ai_message = ChatMessage(role=ChatRole.ASSISTANT, content=response_text)
            session_manager.add_chat_message(request.session_id, ai_message)
            
            # Send response via WebSocket
            await manager.send_personal_message({
                "type": "chat_response",
                "message": response_text,
                "session_id": request.session_id,
                "timestamp": datetime.now().isoformat()
            }, request.session_id)
            
            return ChatResponse(message=response_text, session_id=request.session_id)
        
        # FALLBACK TO FULL AI PROCESSING
        # Process with AI (pass existing session data for modification detection)
        response_text, resume_data = await ai_orchestrator.process_chat_message(
            request.message, session.chat_history, session.user_data
        )
        
        # Add AI response to session
        ai_message = ChatMessage(role=ChatRole.ASSISTANT, content=response_text)
        session_manager.add_chat_message(request.session_id, ai_message)
        
        # If we have resume data, start generating resume
        if resume_data:
            session_manager.update_resume_data(request.session_id, resume_data)
            # Start async resume generation with user query
            asyncio.create_task(generate_and_notify_resume(request.session_id, resume_data, request.message))
        
        # Send response via WebSocket
        await manager.send_personal_message({
            "type": "chat_response",
            "message": response_text,
            "session_id": request.session_id,
            "timestamp": datetime.now().isoformat()
        }, request.session_id)
        
        return ChatResponse(message=response_text, session_id=request.session_id)
        
    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

async def apply_quick_modification(session_id: str, modified_resume: str, user_query: str, impact: str):
    """Apply quick modification without full regeneration"""
    try:
        # Send status update
        await manager.send_personal_message({
            "type": "status_update",
            "message": f"⚡ Applying {impact} modification: {user_query}",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
        # Generate PDF from modified resume using auto-fit generator
        print(f"Applying quick modification for session {session_id}: {user_query}")
        pdf_base64 = pdf_generator.generate_auto_fit_pdf_base64(modified_resume)
        docx_base64 = docx_generator.generate_auto_fit_docx_base64(modified_resume)
        
        if pdf_base64:
            print(f"Quick modification applied successfully, PDF size: {len(pdf_base64)} characters")
            
            # Send updated PDF
            await manager.send_personal_message({
                "type": "resume_pdf_update",
                "pdf_base64": pdf_base64,
                "resume_markdown": modified_resume,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "modification_type": impact
            }, session_id)
            
            # Send updated DOCX if available
            if docx_base64:
                print(f"Quick DOCX modification applied, size: {len(docx_base64)} characters")
                await manager.send_personal_message({
                    "type": "resume_docx_update",
                    "docx_base64": docx_base64,
                    "session_id": session_id,
                    "timestamp": datetime.now().isoformat(),
                    "modification_type": impact
                }, session_id)
            
            # Send completion message
            await manager.send_personal_message({
                "type": "status_update",
                "message": f"✅ {impact.title()} modification applied successfully!",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }, session_id)
        else:
            print("Failed to generate PDF for quick modification")
            await manager.send_personal_message({
                "type": "status_update",
                "message": "❌ Failed to apply modification. Please try again.",
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }, session_id)
            
    except Exception as e:
        print(f"Error in quick modification: {e}")
        await manager.send_personal_message({
            "type": "status_update",
            "message": f"❌ Error applying modification: {str(e)}",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)

async def generate_and_notify_resume(session_id: str, resume_data: ResumeData, user_query: str = ""):
    """Generate resume and notify via WebSocket with status updates"""
    try:
        # Send status update: Starting generation
        await manager.send_personal_message({
            "type": "status_update",
            "message": "🚀 Starting resume generation with modern styling...",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
        # Generate resume markdown with user query
        print(f"Generating resume for session {session_id} with query: {user_query}")
        markdown = await ai_orchestrator.generate_resume_markdown(resume_data, user_query)
        print(f"Resume generated successfully, length: {len(markdown)} characters")
        
        # Send status update: Converting to PDF
        await manager.send_personal_message({
            "type": "status_update",
            "message": "📄 Converting to professional A4 PDF...",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
        # Generate PDF from markdown using auto-fit generator
        print(f"Converting resume to PDF for session {session_id}")
        pdf_base64 = pdf_generator.generate_auto_fit_pdf_base64(markdown)
        if pdf_base64:
            print(f"Auto-fit PDF generated successfully, size: {len(pdf_base64)} characters")
        else:
            print("Failed to generate PDF")
            return
        
        # Also generate DOCX format using auto-fit generator
        print(f"Converting resume to DOCX for session {session_id}")
        docx_base64 = docx_generator.generate_auto_fit_docx_base64(markdown)
        if docx_base64:
            print(f"Auto-fit DOCX generated successfully, size: {len(docx_base64)} characters")
        
        # Update session with both markdown and PDF
        session_manager.update_resume_markdown(session_id, markdown)
        
        # Send PDF update
        await manager.send_personal_message({
            "type": "resume_pdf_update",
            "pdf_base64": pdf_base64,
            "resume_markdown": markdown,  # Keep markdown for backup
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
        # Send DOCX update if generated successfully
        if docx_base64:
            await manager.send_personal_message({
                "type": "resume_docx_update",
                "docx_base64": docx_base64,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }, session_id)
        
        # Send success message
        await manager.send_personal_message({
            "type": "chat_response",
            "message": "✅ Your professional resume has been generated in both PDF and Word formats! Switch between tabs to view different formats. Both are perfect for job applications and ATS systems.",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
    except Exception as e:
        print(f"Error generating resume: {e}")
        # Send error notification
        await manager.send_personal_message({
            "type": "chat_response", 
            "message": f"❌ Sorry, there was an error generating your resume: {str(e)}. Please try again.",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, session_id)
        
        # Try to generate a simple fallback
        try:
            markdown = await ai_orchestrator.generate_resume_markdown(resume_data, "")
            await manager.send_personal_message({
                "type": "resume_update",
                "resume_markdown": markdown,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat()
            }, session_id)
        except:
            pass

@app.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session data"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@app.get("/resume/{session_id}")
async def get_resume(session_id: str):
    """Get resume markdown for a session"""
    session = session_manager.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "session_id": session_id,
        "resume_markdown": session.resume_markdown,
        "last_updated": session.last_updated
    }

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    """WebSocket endpoint for real-time updates"""
    await manager.connect(websocket, session_id)
    try:
        while True:
            # Keep connection alive and listen for any client messages
            data = await websocket.receive_text()
            # Echo back or handle client messages if needed
    except WebSocketDisconnect:
        manager.disconnect(session_id)

@app.post("/generate-docx")
async def generate_docx_endpoint(request: DocxGenerationRequest):
    """Generate DOCX from markdown"""
    try:
        # Validate session
        session = session_manager.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Generate DOCX using auto-fit generator
        print(f"Generating auto-fit DOCX for session {request.session_id}")
        docx_base64 = docx_generator.generate_auto_fit_docx_base64(request.markdown)
        
        if docx_base64:
            print(f"Auto-fit DOCX generated successfully, size: {len(docx_base64)} characters")
            
            # Send update via WebSocket
            await manager.send_personal_message({
                "type": "resume_docx_update",
                "docx_base64": docx_base64,
                "session_id": request.session_id,
                "timestamp": datetime.now().isoformat()
            }, request.session_id)
            
            return DocxResponse(
                docx_base64=docx_base64,
                session_id=request.session_id,
                success=True
            )
        else:
            print("Failed to generate DOCX")
            return DocxResponse(
                docx_base64=None,
                session_id=request.session_id,
                success=False,
                error="Failed to generate DOCX document"
            )
    
    except Exception as e:
        print(f"Error in DOCX generation endpoint: {e}")
        return DocxResponse(
            docx_base64=None,
            session_id=request.session_id,
            success=False,
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=PORT, reload=(ENVIRONMENT == "development"))