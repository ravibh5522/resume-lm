#!/usr/bin/env python3
"""
Pure AI Query Classification System - No regex fallback, 100% AI-powered
"""

import openai
import json
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os
from dotenv import load_dotenv

load_dotenv()

class QueryType(Enum):
    """Types of queries the system can handle"""
    UI_MODIFICATION = "ui_modification"
    CONTENT_UPDATE = "content_update" 
    DATA_GATHERING = "data_gathering"
    RESUME_GENERATION = "resume_generation"
    QUESTION_ANSWER = "question_answer"
    GREETING = "greeting"
    UNCLEAR = "unclear"

@dataclass
class AIQueryClassification:
    """Result of pure AI query classification"""
    query_type: QueryType
    confidence: float
    categories: List[str]
    intent_description: str
    suggested_action: str
    reasoning: str

class PureAIQueryClassifier:
    """100% AI-powered query classification system"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            raise ValueError("Missing OPENAI_API_KEY or OPENAI_BASE_URL environment variables")
            
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    
    async def classify_query(self, message: str, context: Optional[Dict] = None) -> AIQueryClassification:
        """Pure AI-powered query classification with enhanced prompting"""
        
        context_info = ""
        if context:
            context_info = f"""
CONTEXT INFORMATION:
- User has existing resume data: {context.get('has_data', False)}
- Data completeness: {context.get('data_completeness', 0.0)*100:.0f}%
- Previous interactions: {context.get('interaction_count', 0)}
"""
        
        system_prompt = f"""You are an advanced AI query classification expert for a resume generation system. Your job is to understand user intent with 100% accuracy using natural language understanding.

CLASSIFICATION TYPES:

1. UI_MODIFICATION: Visual/styling changes ONLY
   - Font changes (bold, italic, size)
   - Color modifications (blue, navy, professional colors)
   - Layout adjustments (compact, spacious, modern)
   - Spacing changes (tight, loose, organized)
   - Style preferences (professional, creative, clean)
   
2. CONTENT_UPDATE: Modifying existing resume information
   - Changing personal details (name, phone, email)
   - Updating existing experience/education
   - Removing or editing existing content
   - Correcting information already provided
   
3. DATA_GATHERING: User providing NEW information
   - Sharing work experience details
   - Providing education information
   - Listing skills and abilities
   - Describing projects or achievements
   - Any new factual information for the resume
   
4. RESUME_GENERATION: Ready to create/recreate resume
   - Explicit requests to generate resume
   - User indicating they're ready to proceed
   - Requests to see final resume output
   
5. QUESTION_ANSWER: Questions about the system/process
   - How the system works
   - What information is needed
   - Process clarifications
   - Feature explanations
   
6. GREETING: Social interactions
   - Hello, goodbye, thanks
   - Polite conversation starters
   - Acknowledgments and pleasantries
   
7. UNCLEAR: Ambiguous or unclear requests
   - Incomplete thoughts
   - Confusing or contradictory requests
   - Need clarification

ADVANCED CLASSIFICATION RULES:
- For MIXED requests (UI + Content): Prioritize CONTENT_UPDATE
- High confidence (0.9+) for clear, unambiguous requests
- Medium confidence (0.7-0.9) for somewhat clear requests
- Lower confidence (0.5-0.7) for ambiguous requests
- Consider user's conversation history and context
- Understand natural conversational language
- Detect implicit requests and intentions

RESPONSE FORMAT (JSON):
{{
  "query_type": "ui_modification|content_update|data_gathering|resume_generation|question_answer|greeting|unclear",
  "confidence": 0.95,
  "categories": ["specific", "subcategories", "identified"],
  "intent_description": "Detailed description of what the user wants",
  "suggested_action": "Specific action the system should take",
  "reasoning": "Why this classification was chosen over others"
}}

EXAMPLES:

User: "make the name bold"
{{
  "query_type": "ui_modification",
  "confidence": 0.98,
  "categories": ["font", "name", "bold"],
  "intent_description": "User wants the name to appear in bold font formatting",
  "suggested_action": "Apply bold formatting to the name element in the resume",
  "reasoning": "Clear UI modification request with no content changes needed"
}}

User: "I worked at Google for 3 years as a software engineer"
{{
  "query_type": "data_gathering",
  "confidence": 0.99,
  "categories": ["experience", "employment", "tech_industry"],
  "intent_description": "User is providing new work experience information",
  "suggested_action": "Extract and store the employment data: Google, Software Engineer, 3 years",
  "reasoning": "User is sharing factual employment information to be added to resume"
}}

User: "make headers blue and add my Apple experience"
{{
  "query_type": "content_update",
  "confidence": 0.95,
  "categories": ["mixed_request", "ui_modification", "experience"],
  "intent_description": "Mixed request: UI change (blue headers) + content addition (Apple experience)",
  "suggested_action": "Process content addition first, then apply UI modifications",
  "reasoning": "Mixed request prioritizes content changes over UI modifications per system rules"
}}{context_info}

Analyze this user message with deep understanding and provide accurate classification:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f'Classify this message: "{message}"'}
        ]
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,  # type: ignore
                temperature=0.2,  # Lower temperature for more consistent classification
                max_tokens=500
            )
            
            result_text = response.choices[0].message.content or "{}"
            
            # Parse JSON response
            result_data = json.loads(result_text)
            
            return AIQueryClassification(
                query_type=QueryType(result_data.get("query_type", "unclear")),
                confidence=float(result_data.get("confidence", 0.5)),
                categories=result_data.get("categories", []),
                intent_description=result_data.get("intent_description", ""),
                suggested_action=result_data.get("suggested_action", ""),
                reasoning=result_data.get("reasoning", "")
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"AI response parsing error: {e}")
            # Return a reasonable default instead of falling back to regex
            return AIQueryClassification(
                query_type=QueryType.UNCLEAR,
                confidence=0.3,
                categories=["parsing_error"],
                intent_description="Could not parse AI response",
                suggested_action="Request clarification from user",
                reasoning="JSON parsing failed on AI response"
            )
        except Exception as e:
            print(f"AI classification error: {e}")
            return AIQueryClassification(
                query_type=QueryType.UNCLEAR,
                confidence=0.2,
                categories=["system_error"],
                intent_description="System error during classification",
                suggested_action="Retry classification or request clarification",
                reasoning=f"API error: {str(e)}"
            )
    
    def is_ui_only_request(self, classification: AIQueryClassification) -> bool:
        """Check if request is UI-only modification"""
        return (
            classification.query_type == QueryType.UI_MODIFICATION and 
            classification.confidence > 0.7
        )
    
    def is_content_request(self, classification: AIQueryClassification) -> bool:
        """Check if request involves content changes"""
        return classification.query_type in [
            QueryType.CONTENT_UPDATE,
            QueryType.DATA_GATHERING
        ]

class PureAIFunctionManager:
    """Function call manager using pure AI classification"""
    
    def __init__(self):
        self.ai_classifier = PureAIQueryClassifier()
        
        # Function mappings
        self.function_map = {
            QueryType.UI_MODIFICATION: self._handle_ui_modification,
            QueryType.CONTENT_UPDATE: self._handle_content_update,
            QueryType.DATA_GATHERING: self._handle_data_gathering,
            QueryType.RESUME_GENERATION: self._handle_resume_generation,
            QueryType.QUESTION_ANSWER: self._handle_question_answer,
            QueryType.GREETING: self._handle_greeting,
            QueryType.UNCLEAR: self._handle_unclear
        }
    
    async def route_query(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """Route query using pure AI classification"""
        
        classification = await self.ai_classifier.classify_query(message, context)
        
        # Enhanced logging
        print(f"🤖 AI Classification Result:")
        print(f"   Type: {classification.query_type.value}")
        print(f"   Confidence: {classification.confidence:.2f}")
        print(f"   Intent: {classification.intent_description}")
        print(f"   Reasoning: {classification.reasoning}")
        
        handler = self.function_map.get(classification.query_type, self._handle_unclear)
        
        return {
            "classification": classification,
            "result": await handler(message, classification, context)
        }
    
    # Handler methods
    async def _handle_ui_modification(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {
            "action": "ui_modification", 
            "categories": classification.categories,
            "suggested_action": classification.suggested_action
        }
    
    async def _handle_content_update(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {
            "action": "content_update", 
            "categories": classification.categories,
            "suggested_action": classification.suggested_action
        }
    
    async def _handle_data_gathering(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {
            "action": "data_gathering", 
            "categories": classification.categories,
            "suggested_action": classification.suggested_action
        }
    
    async def _handle_resume_generation(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "resume_generation"}
    
    async def _handle_question_answer(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "question_answer"}
    
    async def _handle_greeting(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "greeting"}
    
    async def _handle_unclear(self, message: str, classification: AIQueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "clarification_needed", "reasoning": classification.reasoning}

# Test the pure AI system
if __name__ == "__main__":
    import asyncio
    import time
    
    async def test_pure_ai_system():
        manager = PureAIFunctionManager()
        
        test_messages = [
            # Simple UI modifications
            "make the name bold",
            "change colors to navy blue",
            "use more compact spacing",
            
            # Complex UI requests
            "I want the headers to look more professional with a modern navy blue color scheme",
            "can you make the layout more compact and use larger fonts for section headers?",
            
            # Content updates
            "change my phone number to 555-0123",
            "update my email to john.doe@newcompany.com",
            
            # Data gathering
            "I worked at Tesla as a software engineer for 2 years",
            "My education is from MIT where I got my Computer Science degree",
            "I have skills in Python, React, and machine learning",
            
            # Mixed requests
            "make headers blue and add my Google internship experience",
            "change my name to Jane Smith and make it bold",
            
            # Other types
            "hello, I need help with my resume",
            "generate my resume now",
            "what information do you need from me?",
            "the text looks too small can you make it bigger please",
            
            # Ambiguous
            "make it better",
            "fix this",
        ]
        
        print("🤖 Testing Pure AI Classification System")
        print("=" * 80)
        
        total_time = 0
        results = []
        
        for message in test_messages:
            start_time = time.time()
            result = await manager.route_query(message)
            end_time = time.time()
            
            processing_time = (end_time - start_time) * 1000
            total_time += processing_time
            
            classification = result["classification"]
            
            results.append({
                "message": message,
                "type": classification.query_type.value,
                "confidence": classification.confidence,
                "time_ms": processing_time,
                "categories": classification.categories,
                "reasoning": classification.reasoning
            })
            
            print(f"📝 {message[:60]}{'...' if len(message) > 60 else ''}")
            print(f"   Type: {classification.query_type.value} | Confidence: {classification.confidence:.2f} | Time: {processing_time:.0f}ms")
            print(f"   Categories: {classification.categories}")
            print(f"   Reasoning: {classification.reasoning}")
            print()
        
        avg_time = total_time / len(test_messages)
        high_confidence = sum(1 for r in results if r["confidence"] >= 0.9)
        
        print("📊 PURE AI CLASSIFICATION PERFORMANCE")
        print("=" * 80)
        print(f"🤖 100% AI-powered classification")
        print(f"⏱️  Average processing time: {avg_time:.0f}ms")
        print(f"🎯 High confidence classifications: {high_confidence}/{len(test_messages)} ({high_confidence/len(test_messages)*100:.0f}%)")
        print(f"📈 Total processing time: {total_time:.0f}ms")
        print()
        print("✅ Pure AI Benefits:")
        print("   - Maximum accuracy through deep language understanding")
        print("   - Context-aware classification")
        print("   - Handles complex conversational language")
        print("   - No pattern matching limitations")
        print("   - Detailed reasoning for each classification")
        print("   - Confidence scores for decision making")
        print("   - Natural language intent extraction")
    
    asyncio.run(test_pure_ai_system())