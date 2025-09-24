#!/usr/bin/env python3
"""
Advanced UI Modification Agent - Handles complex UI/styling changes while preserving content
"""

import re
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import openai
from models import ResumeData
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class UIStyleRequest:
    """Represents a UI styling request with specific parameters"""
    element: str      # 'name', 'headers', 'sections', 'layout', 'colors', 'spacing'
    modification: str # 'bold', 'color_change', 'size_increase', 'compact_spacing'
    value: Optional[str] = None
    scope: str = 'specific'  # 'specific', 'global'

class AdvancedUIAgent:
    """Advanced UI agent that handles complex styling without content changes"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            raise ValueError("Missing OPENAI_API_KEY or OPENAI_BASE_URL environment variables")
            
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
        
        # UI modification patterns
        self.ui_keywords = {
            'font': ['font', 'bold', 'italic', 'typeface', 'larger', 'smaller', 'bigger'],
            'color': ['color', 'blue', 'red', 'green', 'navy', 'teal', 'black', 'gray'],
            'layout': ['layout', 'format', 'structure', 'column', 'arrange', 'organize'],
            'spacing': ['spacing', 'compact', 'tight', 'spacious', 'gap', 'margin', 'padding'],
            'size': ['size', 'larger', 'smaller', 'bigger', 'increase', 'decrease'],
            'style': ['style', 'modern', 'professional', 'creative', 'clean', 'minimal']
        }
    
    def is_ui_modification_request(self, message: str) -> bool:
        """Check if the message is requesting UI modifications only"""
        
        message_lower = message.lower()
        
        # Check for UI keywords
        ui_indicators = 0
        content_indicators = 0
        
        # Count UI-related keywords
        for category, keywords in self.ui_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    ui_indicators += 1
        
        # Count content-related keywords (things that would change actual resume data)
        content_keywords = [
            'experience', 'education', 'skills', 'work', 'job', 'company', 'project',
            'degree', 'university', 'college', 'certification', 'add', 'remove',
            'change my', 'update my', 'worked at', 'studied at', 'graduated'
        ]
        
        for keyword in content_keywords:
            if keyword in message_lower:
                content_indicators += 1
        
        # If UI indicators > content indicators, likely a UI request
        return ui_indicators > content_indicators and ui_indicators > 0
    
    async def apply_ui_modifications(self, markdown_content: str, user_request: str, resume_data: Optional[ResumeData] = None) -> str:
        """Apply UI modifications using AI while preserving all content"""
        
        system_prompt = """You are a UI/UX specialist focused ONLY on visual presentation and styling modifications.

CRITICAL RULES:
1. NEVER change any personal information, experience, education, skills, or project content
2. NEVER add or remove resume sections or data points
3. ONLY modify visual presentation, formatting, and styling
4. Preserve ALL existing content exactly as provided
5. Focus ONLY on the visual/styling aspect mentioned in the user request

Your role is to modify ONLY the visual presentation while keeping content identical.

USER REQUEST EXAMPLES AND PROPER RESPONSES:
- "make the name bold" → Only make name bold, change nothing else
- "change header color to blue" → Only change header styling, preserve all content
- "make it more compact" → Only adjust spacing/layout, keep all information
- "use larger font for headers" → Only adjust header sizes, preserve content
- "change layout to be more modern" → Only modify visual structure, keep data identical

FORBIDDEN ACTIONS:
- Changing names, phone numbers, emails, addresses
- Modifying job titles, company names, dates, descriptions
- Adding or removing skills, experiences, projects
- Changing educational information
- Altering any factual content

MARKDOWN STYLING TOOLS AVAILABLE:
- Headers: # ## ###
- Bold: **text**
- Italic: *text*
- Lists: - or * for bullets
- Horizontal rules: ---
- Line breaks for spacing
- Unicode symbols for visual enhancement (sparingly)
- Tables for structured layout

Return ONLY the modified markdown with requested styling changes applied."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"ORIGINAL RESUME:\n{markdown_content}\n\nUSER STYLING REQUEST: {user_request}\n\nApply ONLY the requested visual/styling changes while preserving ALL content exactly."}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=0.3,  # Lower temperature for precise modifications
                max_tokens=4000
            )
            
            modified_content = response.choices[0].message.content or markdown_content
            
            # Verify content integrity
            if self._content_integrity_check(markdown_content, modified_content):
                return modified_content
            else:
                print("⚠️  Content integrity check failed, returning original content")
                return markdown_content
                
        except Exception as e:
            print(f"UI modification error: {e}")
            return markdown_content
    
    def _content_integrity_check(self, original: str, modified: str) -> bool:
        """Basic check to ensure content wasn't changed inappropriately"""
        
        # Extract key content elements for comparison
        original_lines = [line.strip() for line in original.split('\n') if line.strip()]
        modified_lines = [line.strip() for line in modified.split('\n') if line.strip()]
        
        # Check if significant content was removed (allow for styling changes)
        original_content_words = len([word for line in original_lines for word in line.split() if not word.startswith('#')])
        modified_content_words = len([word for line in modified_lines for word in line.split() if not word.startswith('#')])
        
        # Allow up to 10% word count difference for styling modifications
        word_diff_ratio = abs(original_content_words - modified_content_words) / max(original_content_words, 1)
        
        return word_diff_ratio < 0.1  # Less than 10% difference is acceptable
    
    def get_ui_modification_categories(self, message: str) -> List[str]:
        """Get the categories of UI modifications requested"""
        
        message_lower = message.lower()
        categories = []
        
        for category, keywords in self.ui_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                categories.append(category)
        
        return categories

# Enhanced UI modification prompt generator
def create_advanced_ui_prompt(original_content: str, user_request: str, resume_data: Optional[ResumeData] = None) -> str:
    """Create an advanced prompt for UI modifications with content protection"""
    
    content_summary = ""
    if resume_data:
        content_summary = f"""
PROTECTED CONTENT SUMMARY (DO NOT MODIFY):
- Name: {resume_data.profile.name if resume_data.profile.name else 'Not specified'}
- Contact: {len([x for x in [resume_data.profile.email, resume_data.profile.phone, resume_data.profile.location] if x])} contact fields
- Experience: {len(resume_data.experience)} entries
- Education: {len(resume_data.education)} entries  
- Skills: {len(resume_data.skills)} items
- Projects: {len(resume_data.projects)} entries
"""
    
    return f"""
You are a UI/UX specialist. Your ONLY job is to modify visual presentation.

{content_summary}

ORIGINAL RESUME:
{original_content}

USER REQUEST: {user_request}

TASK: Apply ONLY the visual/styling changes requested. DO NOT change any actual content, data, or information.

VISUAL TOOLS AVAILABLE:
- Markdown headers (# ## ###)
- Bold (**text**) and italic (*text*)
- Bullet points with symbols
- Horizontal rules (---)
- Spacing with line breaks
- Unicode symbols for visual enhancement
- Tables for layout

RETURN: Modified markdown with ONLY visual changes applied.
"""

# Test the advanced UI agent
if __name__ == "__main__":
    agent = AdvancedUIAgent()
    
    test_messages = [
        "make the name bold",
        "can you add more experience at Google?",  # This should NOT be UI
        "change the color scheme to blue",
        "I worked at Microsoft for 3 years",  # This should NOT be UI
        "make the layout more compact",
        "larger font size for headers"
    ]
    
    print("🎨 Testing Advanced UI Detection")
    print("=" * 50)
    
    for msg in test_messages:
        is_ui = agent.is_ui_modification_request(msg)
        categories = agent.get_ui_modification_categories(msg)
        
        if is_ui:
            print(f"✅ UI Request: '{msg}' → Categories: {categories}")
        else:
            print(f"❌ Content Request: '{msg}' → Not UI modification")
    
    print(f"\n🔧 Advanced UI Agent Ready!")
    print("Features:")
    print("- Content integrity protection")
    print("- AI-powered visual modifications")
    print("- Category-based UI detection")
    print("- Precision styling adjustments")