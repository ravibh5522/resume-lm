from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class ChatRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class FileAttachment(BaseModel):
    filename: str
    file_type: str  # 'image' or 'pdf'
    content: str    # base64 encoded content
    mime_type: str  # e.g., 'image/jpeg', 'application/pdf'
    extracted_text: Optional[str] = None  # For PDFs

class ChatMessage(BaseModel):
    role: ChatRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    attachments: List[FileAttachment] = []

class UserProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None
    
class Experience(BaseModel):
    company: str
    position: str
    start_date: str
    end_date: Optional[str] = None
    description: List[str] = []
    location: Optional[str] = None

class Education(BaseModel):
    institution: str
    degree: str
    field: Optional[str] = "General Studies"
    start_date: str
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    location: Optional[str] = None

class Project(BaseModel):
    name: str
    description: str
    technologies: List[str] = []
    url: Optional[str] = None
    github: Optional[str] = None

class ResumeData(BaseModel):
    profile: UserProfile = Field(default_factory=UserProfile)
    summary: Optional[str] = None
    experience: List[Experience] = []
    education: List[Education] = []
    skills: List[str] = []
    projects: List[Project] = []
    certifications: List[str] = []
    languages: List[str] = []

class SessionData(BaseModel):
    session_id: str
    user_data: ResumeData = Field(default_factory=ResumeData)
    chat_history: List[ChatMessage] = []
    resume_markdown: Optional[str] = None
    last_updated: datetime = Field(default_factory=datetime.now)
    status: str = "active"

class ChatRequest(BaseModel):
    message: str
    session_id: str
    attachments: List[FileAttachment] = []

class DocxGenerationRequest(BaseModel):
    markdown: str
    session_id: str

class ChatResponse(BaseModel):
    message: str
    session_id: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DocxResponse(BaseModel):
    docx_base64: Optional[str]
    session_id: str
    success: bool = True
    error: Optional[str] = None

class ResumeUpdateEvent(BaseModel):
    session_id: str
    resume_markdown: str
    timestamp: datetime = Field(default_factory=datetime.now)
    event_type: str = "resume_update"

# Structured Output Models for OpenAI API
class StructuredResumeData(BaseModel):
    """Structured output model for data gathering agent"""
    profile: UserProfile
    summary: str
    experience: List[Experience]
    education: List[Education] 
    skills: List[str]
    projects: List[Project]
    certifications: List[str] = []
    languages: List[str] = []
    ready_to_generate: bool = True

class DataGatheringResponse(BaseModel):
    """Response model for data gathering conversations"""
    message: str
    collected_data: Optional[StructuredResumeData] = None
    needs_more_info: bool = True

class ResumeGeneratorResponse(BaseModel):
    """Structured output model for resume generation"""
    markdown_resume: str = Field(description="The complete markdown resume content")
    design_notes: Optional[str] = Field(default=None, description="Brief notes about the design choices made")
    word_count: Optional[int] = Field(default=None, description="Approximate word count of the resume")