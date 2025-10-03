#!/usr/bin/env python3
"""
Dynamic Section Manager
Handles flexible resume sections based on candidate data and AI decisions
"""

from typing import List, Dict, Any, Optional, Tuple
from models import DynamicSection, ResumeData, Experience, Education, Project
import json

class SectionManager:
    """Manages dynamic resume sections based on content and candidate needs"""
    
    def __init__(self):
        self.section_types = {
            "experience": {
                "default_title": "Professional Experience",
                "content_type": "experience",
                "required_fields": ["company", "position"],
                "icon": "💼"
            },
            "education": {
                "default_title": "Education",
                "content_type": "education", 
                "required_fields": ["institution", "degree"],
                "icon": "🎓"
            },
            "skills": {
                "default_title": "Technical Skills",
                "content_type": "list",
                "required_fields": [],
                "icon": "⚡"
            },
            "projects": {
                "default_title": "Key Projects",
                "content_type": "projects",
                "required_fields": ["name"],
                "icon": "🚀"
            },
            "certifications": {
                "default_title": "Certifications",
                "content_type": "list",
                "required_fields": [],
                "icon": "📜"
            },
            "languages": {
                "default_title": "Languages",
                "content_type": "list",
                "required_fields": [],
                "icon": "🌐"
            },
            "awards": {
                "default_title": "Awards & Honors",
                "content_type": "list",
                "required_fields": [],
                "icon": "🏆"
            },
            "publications": {
                "default_title": "Publications",
                "content_type": "list",
                "required_fields": [],
                "icon": "📚"
            },
            "volunteer": {
                "default_title": "Volunteer Experience",
                "content_type": "experience",
                "required_fields": ["organization"],
                "icon": "🤝"
            },
            "leadership": {
                "default_title": "Leadership Experience",
                "content_type": "experience",
                "required_fields": ["organization", "role"],
                "icon": "👑"
            }
        }
        
        self.default_section_order = [
            "experience", "education", "skills", "projects", 
            "certifications", "awards", "publications", "volunteer",
            "leadership", "languages"
        ]
    
    def determine_sections(self, candidate_data: Dict[str, Any]) -> List[str]:
        """Determine appropriate sections based on candidate data"""
        sections = []
        message = candidate_data.get('message', '').lower()
        
        # Always include core sections
        sections.extend(['experience', 'education', 'skills'])
        
        # Conditional sections based on content
        if any(word in message for word in ['project', 'built', 'developed', 'created']):
            sections.append('projects')
        
        if any(word in message for word in ['award', 'recognition', 'honor', 'winner']):
            sections.append('awards')
        
        if any(word in message for word in ['published', 'paper', 'research', 'publication']):
            sections.append('publications')
        
        if any(word in message for word in ['volunteer', 'community', 'nonprofit']):
            sections.append('volunteer')
        
        if any(word in message for word in ['lead', 'manage', 'captain', 'president']):
            sections.append('leadership')
        
        if any(word in message for word in ['certified', 'certification', 'license']):
            sections.append('certifications')
        
        if any(word in message for word in ['language', 'fluent', 'bilingual']):
            sections.append('languages')
        
        return list(set(sections))  # Remove duplicates
    
    def create_section(self, title: str, content_type: str, content: Any, order: int = 0) -> DynamicSection:
        """Create a new dynamic section"""
        return DynamicSection(
            title=title,
            content_type=content_type,
            content=content,
            order=order
        )
    
    def format_section_content(self, section_type: str, raw_content: Any) -> str:
        """Format raw content for a specific section type"""
        if section_type == "experience":
            if isinstance(raw_content, list):
                return f"{len(raw_content)} professional experiences"
            return "Professional experience details"
        
        elif section_type == "skills":
            if isinstance(raw_content, list):
                return ", ".join(raw_content)
            return str(raw_content)
        
        elif section_type == "projects":
            if isinstance(raw_content, list):
                return f"{len(raw_content)} notable projects"
            return "Project details"
        
        else:
            return str(raw_content)\n