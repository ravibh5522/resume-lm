import asyncio
import json
import openai
from typing import Dict, Any, Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv
from models import (
    ResumeData, ChatMessage, ChatRole, UserProfile, Experience, 
    Education, Project, DataGatheringResponse, StructuredResumeData,
    ResumeGeneratorResponse
)

load_dotenv()

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            raise ValueError("Missing OPENAI_API_KEY or OPENAI_BASE_URL environment variables")
            
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    
    async def get_completion(self, messages: List[Dict[str, Any]], temperature: float = 0.7) -> str:
        """Get completion from OpenAI API (legacy method for resume generation)"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_tokens=3000
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return f"I apologize, but I'm experiencing technical difficulties. Please try again later."
    
    def get_parsed_completion(self, messages, response_format):
        """Get completion with structured output using response.parsed"""
        try:
            response = self.client.chat.completions.parse(
                model=self.model,  # Use the configured model
                messages=messages,
                response_format=response_format
            )
            return response.choices[0].message.parsed
        except Exception as e:
            print(f"OpenAI parsed API error: {e}")
            # Fallback to JSON mode
            response = self.client.chat.completions.create(
                model=self.model,  # Use the configured model
                messages=messages,
                response_format={"type": "json_object"}
            )
            import json
            return json.loads(response.choices[0].message.content or "{}")
    
    async def get_structured_completion(self, messages: List[Dict[str, Any]], schema_description: str, temperature: float = 0.7):
        """Get structured completion using JSON mode with schema instructions (fallback)"""
        try:
            # Add JSON schema instruction to the system message
            if messages and messages[0]["role"] == "system":
                messages[0]["content"] += f"\n\nIMPORTANT: {schema_description}"
            else:
                messages.insert(0, {"role": "system", "content": schema_description})
            
            # Use regular completion without response_format for compatibility
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=temperature,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            if content:
                try:
                    return json.loads(content)
                except json.JSONDecodeError:
                    # If JSON parsing fails, try to extract JSON from the content
                    import re
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        return json.loads(json_match.group())
            return None
        except Exception as e:
            print(f"OpenAI structured API error: {e}")
            return None

class DataGatheringAgent:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.system_prompt = """You are a professional resume consultant assistant. Your role is to gather comprehensive information from users to create outstanding resumes.

CONVERSATION FLOW:
1. Ask targeted questions to collect user information
2. Be conversational and helpful
3. When user says "generate", "create", or you have sufficient info, proceed to generate

KEY TRIGGERS FOR GENERATION:
- User explicitly says "generate", "create resume", "make resume"
- User provides complete random/sample data request
- You have collected sufficient basic information
- User requests modifications to existing resume (change font, layout, styling, format, colors, etc.)
- User asks to update/modify/change any aspect of an already generated resume

You should ask targeted questions to collect:
1. Personal Information (name, email, phone, location, LinkedIn, GitHub, website)
2. Professional Summary/Objective  
3. Work Experience (company, position, dates, responsibilities, achievements)
4. Education (institution, degree, field, dates, GPA if relevant)
5. Skills (technical, soft skills, languages, certifications)
6. Projects (name, description, technologies used, URLs)
7. Additional sections (certifications, languages, volunteer work, awards)

Guidelines:
- Ask 1-3 questions at a time to avoid overwhelming the user
- Be conversational and friendly
- Focus on achievements and quantifiable results
- Probe for specific details when answers are vague
- Guide users to highlight their strengths
- If user wants a sample/random resume, create one immediately

When ready to generate, be clear about the next steps."""
        
        self.schema_description = """Respond with a JSON object containing:
{
  "message": "string - your conversational response to the user",
  "collected_data": {
    "profile": {
      "name": "string or null",
      "email": "string or null", 
      "phone": "string or null",
      "location": "string or null",
      "linkedin": "string or null",
      "github": "string or null",
      "website": "string or null"
    },
    "summary": "string - professional summary",
    "experience": [
      {
        "company": "string",
        "position": "string", 
        "start_date": "string",
        "end_date": "string or null",
        "description": ["string", "string"],
        "location": "string or null"
      }
    ],
    "education": [
      {
        "institution": "string",
        "degree": "string",
        "field": "string", 
        "start_date": "string",
        "end_date": "string or null",
        "gpa": "string or null",
        "location": "string or null"
      }
    ],
    "skills": ["string", "string"],
    "projects": [
      {
        "name": "string",
        "description": "string",
        "technologies": ["string", "string"],
        "url": "string or null",
        "github": "string or null"
      }
    ],
    "certifications": ["string", "string"],
    "languages": ["string", "string"],
    "ready_to_generate": false
  },
  "needs_more_info": true
}

Set ready_to_generate to true and needs_more_info to false only when you have sufficient information for a complete resume."""
    
    async def process_message(self, message: str, chat_history: List[ChatMessage]) -> tuple[str, Optional[ResumeData]]:
        """Process user message and return response and optional resume data"""
        
        # Convert chat history to OpenAI format
        messages = [{"role": "system", "content": self.system_prompt}]
        
        for chat in chat_history[-10:]:  # Last 10 messages for context
            messages.append({
                "role": chat.role.value,
                "content": chat.content
            })
        
        messages.append({"role": "user", "content": message})
        
        # Try structured output with response.parsed first
        try:
            from models import DataGatheringResponse
            parsed_data = self.openai_client.get_parsed_completion(
                messages, DataGatheringResponse
            )
            
            if parsed_data:
                message_text = parsed_data.message
                collected_data = parsed_data.collected_data
                needs_more_info = parsed_data.needs_more_info
                
                # Check if we should generate resume
                if collected_data and not needs_more_info and collected_data.ready_to_generate:
                    # Convert StructuredResumeData to ResumeData
                    resume_data = ResumeData(
                        profile=collected_data.profile,
                        summary=collected_data.summary,
                        experience=collected_data.experience,
                        education=collected_data.education,
                        skills=collected_data.skills,
                        projects=collected_data.projects,
                        certifications=collected_data.certifications,
                        languages=collected_data.languages
                    )
                    return "Perfect! I have all the information needed. I'm now generating your professional resume with modern styling and visual elements. Please wait a moment...", resume_data
                
                return message_text, None
        except Exception as e:
            print(f"Error with parsed response: {e}")
        
        # Fallback to structured completion with JSON schema
        structured_response = await self.openai_client.get_structured_completion(
            messages, self.schema_description, temperature=0.7
        )
        
        if structured_response:
            try:
                message_text = structured_response.get("message", "")
                collected_data = structured_response.get("collected_data")
                needs_more_info = structured_response.get("needs_more_info", True)
                
                # Check if we should generate resume
                if collected_data and not needs_more_info and collected_data.get("ready_to_generate"):
                    # Convert to ResumeData
                    resume_data = ResumeData.model_validate(collected_data)
                    return "Perfect! I have all the information needed. I'm now generating your professional resume with modern styling and visual elements. Please wait a moment...", resume_data
                
                return message_text, None
            except Exception as e:
                print(f"Error processing structured response: {e}")
        
        # Final fallback to regular completion with simple parsing
        response = await self.openai_client.get_completion(messages)
        
        # Check if the response indicates readiness to generate
        if "ready_to_generate" in response.lower() or "generate" in message.lower():
            # Try to extract basic data for resume generation
            try:
                # Create a basic resume data structure
                basic_data = ResumeData(
                    profile=UserProfile(
                        name="Sample User",
                        email="user@example.com",
                        phone="+1-234-567-8900",
                        location="Your City, Country"
                    ),
                    summary="Recent graduate with strong technical skills and passion for innovation.",
                    skills=["Python", "JavaScript", "Problem Solving", "Communication"],
                    education=[Education(
                        institution="Your University",
                        degree="Bachelor of Technology", 
                        field="Computer Science",
                        start_date="2019",
                        end_date="2023"
                    )],
                    projects=[Project(
                        name="Portfolio Website",
                        description="Personal website showcasing projects and skills",
                        technologies=["HTML", "CSS", "JavaScript"]
                    )]
                )
                return "Great! I'm generating a sample resume for you with modern styling. You can customize it later...", basic_data
            except Exception as e:
                print(f"Error creating basic resume data: {e}")
        
        return response, None
    
    def extract_resume_data(self, response: str) -> Optional[ResumeData]:
        """Extract resume data if the agent signals it's ready (fallback method)"""
        if "READY_TO_GENERATE_RESUME:" in response:
            try:
                json_str = response.split("READY_TO_GENERATE_RESUME:")[1].strip()
                data = json.loads(json_str)
                return ResumeData.model_validate(data)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error parsing resume data: {e}")
                return None
        return None

class ResumeGeneratorAgent:
    def __init__(self, openai_client: OpenAIClient):
        self.openai_client = openai_client
        self.system_prompt = """You are an elite resume writer specializing in creating visually stunning, modern resumes using PURE MARKDOWN formatting.

CRITICAL: Generate ONLY clean markdown content - NO HTML tags, NO inline CSS, NO <div> or <span> elements.

STRUCTURED OUTPUT INSTRUCTIONS:
- Return your response as a structured ResumeGeneratorResponse object
- The 'markdown_resume' field should contain ONLY clean markdown content
- Use modern visual design elements within markdown limitations
- Focus on quantifiable achievements and impact metrics
- RESPOND TO USER REQUIREMENTS: Pay special attention to any user-specific requests for layout changes, formatting preferences, styling modifications, or content adjustments

Create a resume with:
🎨 MODERN VISUAL DESIGN (Markdown Only):
- Create visual hierarchy with markdown headers (# ## ###)
- Use horizontal rules (---) for section separators
- Use bold (**text**) and italic (*text*) for emphasis
- Use bullet points with modern symbols (▪, ◆, ⚡, 🔹) instead of plain -
- Use Unicode symbols sparingly for section headers only

✨ CONTEMPORARY FORMATTING (Markdown Only):
- Clean name header WITHOUT emojis (just # Name)
- Contact information on SINGLE LINE separated by | (pipe symbols)
- Section headers with minimal emoji usage (⚡ for skills, 💼 for experience, 🎓 for education)
- Bullet points with modern Unicode symbols
- Strategic use of **bold** and *italic* for emphasis
- Professional structure using markdown tables where appropriate
- Clean layout with proper spacing using line breaks

HEADER FORMAT EXAMPLE:
# John Smith
Location | Phone | Email | LinkedIn | GitHub

🚀 CONTENT EXCELLENCE:
- Achievement-focused bullet points with quantifiable results
- Action verbs and industry keywords for ATS optimization
- Compelling professional summary that tells a story
- Technical skills organized by category with visual separators
- Project descriptions that showcase impact and innovation

📱 RESPONSIVE DESIGN THINKING:
- Clean, scannable markdown layout
- Logical information hierarchy using markdown headers
- White space utilization for readability
- Professional yet modern aesthetic using only markdown

🎯 USER RESPONSIVENESS:
- If user requests specific layout changes (e.g., "make it more compact", "add more sections", "change the order"), implement those changes
- If user asks for style modifications (e.g., "use different colors", "more professional", "more creative"), adapt the visual elements accordingly
- If user wants content changes (e.g., "emphasize technical skills", "highlight leadership experience"), adjust the content focus
- Always maintain professional quality while accommodating user preferences

IMPORTANT: The markdown_resume field should contain ONLY pure markdown content with no HTML elements whatsoever."""
    
    async def generate_resume(self, resume_data: ResumeData, user_query: str = "") -> str:
        """Generate modern, visually appealing markdown resume from structured data"""
        
        # Create a comprehensive, modern prompt for the AI
        user_data_prompt = self._create_enhanced_prompt(resume_data, user_query)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_data_prompt}
        ]
        
        try:
            # Use structured output with response.parsed
            structured_response = self.openai_client.get_parsed_completion(
                messages, ResumeGeneratorResponse
            )
            
            if structured_response and hasattr(structured_response, 'markdown_resume'):
                return structured_response.markdown_resume
            else:
                # Fallback to legacy method if structured response fails
                print("⚠️ Structured output failed, using fallback method")
                return await self.openai_client.get_completion(messages, temperature=0.2)
                
        except Exception as e:
            print(f"⚠️ Resume generation error: {e}, using fallback method")
            # Fallback to legacy method
            return await self.openai_client.get_completion(messages, temperature=0.2)
    
    def _create_enhanced_prompt(self, resume_data: ResumeData, user_query: str = "") -> str:
        """Create an enhanced prompt with rich context for modern resume generation"""
        
        # Determine field/industry for targeted keywords
        field_context = self._determine_field_context(resume_data)
        
        # Add user query section if provided
        user_requirements = ""
        if user_query.strip():
            user_requirements = f"""
� USER SPECIFIC REQUIREMENTS:
The user has made a specific request: "{user_query}"
Please incorporate these requirements into the resume design, layout, style, or content as appropriate.
Pay special attention to any layout changes, formatting preferences, or styling requests mentioned.

"""
        
        prompt = f"""
�🎯 CREATE A MODERN, VISUALLY STUNNING RESUME FOR:

{user_requirements}👤 PROFESSIONAL PROFILE:
{self._format_profile_enhanced(resume_data.profile)}

💼 CAREER NARRATIVE: 
{resume_data.summary or 'Craft a compelling summary that tells their professional story, highlighting key strengths and career trajectory based on their experience below.'}

🌟 PROFESSIONAL EXPERIENCE:
{self._format_experience_enhanced(resume_data.experience)}

🎓 EDUCATIONAL BACKGROUND:
{self._format_education_enhanced(resume_data.education)}

⚡ TECHNICAL EXPERTISE:
{self._format_skills_enhanced(resume_data.skills, field_context)}

🚀 NOTABLE PROJECTS:
{self._format_projects_enhanced(resume_data.projects)}

📜 CERTIFICATIONS & ACHIEVEMENTS:
{self._format_certifications_enhanced(resume_data.certifications)}

🌍 LANGUAGES:
{self._format_languages_enhanced(resume_data.languages)}

DESIGN REQUIREMENTS:
- Use modern visual elements (symbols, emojis, dividers)
- Create clear visual hierarchy with strategic typography
- Implement professional color scheme suggestions
- Ensure ATS compatibility while maintaining visual appeal
- Focus on quantifiable achievements and impact metrics
- Use contemporary formatting with clean spacing
"""
        return prompt
    
    def _determine_field_context(self, resume_data: ResumeData) -> str:
        """Determine the professional field based on skills and experience"""
        skills_text = ' '.join(resume_data.skills).lower()
        exp_text = ' '.join([f"{exp.position} {' '.join(exp.description)}" for exp in resume_data.experience]).lower()
        
        tech_keywords = ['python', 'javascript', 'react', 'node', 'sql', 'aws', 'docker', 'kubernetes']
        design_keywords = ['design', 'ui', 'ux', 'figma', 'adobe', 'photoshop']
        business_keywords = ['management', 'strategy', 'marketing', 'sales', 'analytics']
        
        combined_text = skills_text + ' ' + exp_text
        
        if any(keyword in combined_text for keyword in tech_keywords):
            return "technology"
        elif any(keyword in combined_text for keyword in design_keywords):
            return "design"
        elif any(keyword in combined_text for keyword in business_keywords):
            return "business"
        else:
            return "general"
    
    def _format_profile_enhanced(self, profile: UserProfile) -> str:
        """Format profile with enhanced presentation"""
        items = []
        if profile.name: items.append(f"Name: {profile.name}")
        if profile.email: items.append(f"Email: {profile.email}")
        if profile.phone: items.append(f"Phone: {profile.phone}")
        if profile.location: items.append(f"Location: {profile.location}")
        if profile.linkedin: items.append(f"LinkedIn: {profile.linkedin}")
        if profile.github: items.append(f"GitHub: {profile.github}")
        if profile.website: items.append(f"Website: {profile.website}")
        
        return '\n'.join(items) if items else "Create professional contact header"
    
    def _format_experience_enhanced(self, experience: List[Experience]) -> str:
        """Format experience with enhanced presentation and impact focus"""
        if not experience:
            return "No experience provided - create a section if needed"
        
        formatted = []
        for i, exp in enumerate(experience, 1):
            exp_block = f"""
ROLE {i}:
• Position: {exp.position}
• Company: {exp.company}
• Duration: {exp.start_date} to {exp.end_date or 'Present'}
• Location: {exp.location or 'Not specified'}
• Key Achievements: {'; '.join(exp.description) if exp.description else 'Develop achievement-focused bullet points based on role'}
"""
            formatted.append(exp_block)
        
        return '\n'.join(formatted)
    
    def _format_education_enhanced(self, education: List[Education]) -> str:
        """Format education with enhanced presentation"""
        if not education:
            return "No education provided - include if relevant"
        
        formatted = []
        for i, edu in enumerate(education, 1):
            edu_block = f"""
EDUCATION {i}:
• Degree: {edu.degree} in {edu.field}
• Institution: {edu.institution}
• Duration: {edu.start_date} to {edu.end_date or 'Present'}
• Location: {edu.location or 'Not specified'}
• GPA: {edu.gpa or 'Not provided'}
"""
            formatted.append(edu_block)
        
        return '\n'.join(formatted)
    
    def _format_skills_enhanced(self, skills: List[str], field_context: str) -> str:
        """Format skills with categorization and field-specific enhancement"""
        if not skills:
            return "No skills provided - organize by category (Programming Languages, Frameworks, Tools, etc.)"
        
        skills_context = f"""
Skills to organize and enhance: {', '.join(skills)}
Field Context: {field_context}
Create logical categories and add relevant complementary skills for this field."""
        return skills_context
    
    def _format_projects_enhanced(self, projects: List[Project]) -> str:
        """Format projects with enhanced presentation and impact focus"""
        if not projects:
            return "No projects provided - include if relevant"
        
        formatted = []
        for i, proj in enumerate(projects, 1):
            proj_block = f"""
PROJECT {i}:
• Name: {proj.name}
• Description: {proj.description}
• Technologies: {', '.join(proj.technologies) if proj.technologies else 'Not specified'}
• Live Demo: {proj.url or 'Not provided'}
• Source Code: {proj.github or 'Not provided'}
"""
            formatted.append(proj_block)
        
        return '\n'.join(formatted)
    
    def _format_certifications_enhanced(self, certifications: List[str]) -> str:
        """Format certifications with enhanced presentation"""
        if not certifications:
            return "No certifications provided - include if relevant"
        return f"Certifications to format professionally: {', '.join(certifications)}"
    
    def _format_languages_enhanced(self, languages: List[str]) -> str:
        """Format languages with enhanced presentation"""
        if not languages:
            return "No languages provided - include if relevant"
        return f"Languages to format with proficiency levels: {', '.join(languages)}"
    
class AIAgentOrchestrator:
    def __init__(self):
        self.openai_client = OpenAIClient()
        self.data_gathering_agent = DataGatheringAgent(self.openai_client)
        self.resume_generator_agent = ResumeGeneratorAgent(self.openai_client)
    
    async def process_chat_message(self, message: str, chat_history: List[ChatMessage], existing_resume_data: Optional[ResumeData] = None) -> tuple[str, Optional[ResumeData]]:
        """Process chat message and return response and optional resume data if ready"""
        
        # Check if this is a modification request for existing resume
        modification_keywords = ['change', 'modify', 'update', 'font', 'style', 'color', 'layout', 'format', 'make it', 'can you']
        is_modification_request = any(keyword in message.lower() for keyword in modification_keywords)
        
        if existing_resume_data and existing_resume_data.profile.name and is_modification_request:
            # This is a modification request for an existing resume
            return f"Perfect! I understand you want to modify your existing resume. I'm regenerating it with your requested changes: '{message}'. Please wait a moment...", existing_resume_data
        
        response_text, resume_data = await self.data_gathering_agent.process_message(message, chat_history)
        
        if resume_data:
            # Clean up the response if it contains old-style markers
            if "READY_TO_GENERATE_RESUME:" in response_text:
                clean_response = response_text.split("READY_TO_GENERATE_RESUME:")[0].strip()
                if not clean_response:
                    clean_response = "Great! I have all the information I need. I'm now generating your professional resume."
                return clean_response, resume_data
            return response_text, resume_data
        
        return response_text, None
    
    async def generate_resume_markdown(self, resume_data: ResumeData, user_query: str = "") -> str:
        """Generate resume markdown from structured data with enhanced performance"""
        return await self.resume_generator_agent.generate_resume(resume_data, user_query)