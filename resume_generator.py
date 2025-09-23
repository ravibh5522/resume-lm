import asyncio
from typing import Optional
from models import ResumeData, SessionData
from agents import AIAgentOrchestrator
from session_manager import SessionManager

class ResumeGenerationService:
    def __init__(self, session_manager: SessionManager):
        self.session_manager = session_manager
        self.ai_orchestrator = AIAgentOrchestrator()
    
    async def generate_resume_async(self, session_id: str, resume_data: ResumeData) -> bool:
        """Generate resume markdown asynchronously and update session"""
        try:
            # Generate the resume markdown
            markdown = await self.ai_orchestrator.generate_resume_markdown(resume_data)
            
            # Update session with the generated resume
            success = self.session_manager.update_resume_markdown(session_id, markdown)
            
            if success:
                print(f"Resume generated successfully for session {session_id}")
                return True
            else:
                print(f"Failed to update session {session_id} with resume")
                return False
                
        except Exception as e:
            print(f"Error generating resume for session {session_id}: {e}")
            return False
    
    def start_resume_generation(self, session_id: str, resume_data: ResumeData):
        """Start resume generation in background"""
        asyncio.create_task(self.generate_resume_async(session_id, resume_data))