#!/usr/bin/env python3
"""
Intelligent Query Classification System - AI-powered query type detection
Replaces regex-heavy keyword matching with smarter classification
"""

import openai
import json
from typing import Dict, List, Optional, Any, Literal
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

class UICategory(Enum):
    """Categories of UI modifications"""
    FONT = "font"
    COLOR = "color"
    LAYOUT = "layout"
    SPACING = "spacing"
    SIZE = "size"
    STYLE = "style"

class ContentCategory(Enum):
    """Categories of content modifications"""
    PERSONAL_INFO = "personal_info"
    EXPERIENCE = "experience"
    EDUCATION = "education"
    SKILLS = "skills"
    PROJECTS = "projects"
    SUMMARY = "summary"

@dataclass
class QueryClassification:
    """Result of query classification"""
    query_type: QueryType
    confidence: float
    categories: List[str]
    intent_description: str
    suggested_action: str

class IntelligentQueryClassifier:
    """AI-powered query classification system"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("OPENAI_BASE_URL")
        
        if not api_key or not base_url:
            raise ValueError("Missing OPENAI_API_KEY or OPENAI_BASE_URL environment variables")
            
        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
        
        # Fallback patterns for when AI is unavailable
        self.fallback_patterns = {
            QueryType.UI_MODIFICATION: [
                'bold', 'italic', 'color', 'blue', 'red', 'layout', 'compact', 
                'spacing', 'font', 'larger', 'smaller', 'style', 'modern', 'professional'
            ],
            QueryType.CONTENT_UPDATE: [
                'add experience', 'change name', 'update skills', 'worked at',
                'studied at', 'graduated', 'add project', 'remove', 'delete'
            ],
            QueryType.DATA_GATHERING: [
                'tell me', 'what', 'how', 'my name is', 'I worked', 'I studied',
                'my skills', 'I have experience'
            ],
            QueryType.GREETING: [
                'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'thanks'
            ]
        }
    
    async def classify_query(self, message: str, context: Optional[Dict] = None) -> QueryClassification:
        """Classify user query using AI with fallback to pattern matching"""
        
        try:
            return await self._ai_classify_query(message, context)
        except Exception as e:
            print(f"AI classification failed: {e}, using fallback")
            return self._fallback_classify_query(message)
    
    async def _ai_classify_query(self, message: str, context: Optional[Dict] = None) -> QueryClassification:
        """AI-powered query classification"""
        
        context_info = ""
        if context:
            context_info = f"\nCONTEXT: User has existing resume data: {context.get('has_data', False)}"
        
        system_prompt = f"""You are a query classification expert for an AI resume generator system.

Classify user messages into these types:

1. UI_MODIFICATION: Visual/styling changes only (colors, fonts, layout, spacing)
   - Examples: "make it bold", "use blue color", "more compact layout"
   
2. CONTENT_UPDATE: Modifying existing resume data
   - Examples: "change my name", "update my phone", "add experience at Google"
   
3. DATA_GATHERING: Providing new information for resume
   - Examples: "I worked at Microsoft", "My name is John", "I have Python skills"
   
4. RESUME_GENERATION: Ready to generate or regenerate resume
   - Examples: "generate my resume", "create resume now", "I'm ready"
   
5. QUESTION_ANSWER: Questions about the system or process
   - Examples: "How does this work?", "What information do you need?"
   
6. GREETING: Social interaction
   - Examples: "hello", "thanks", "goodbye"
   
7. UNCLEAR: Ambiguous or unclear intent

RESPONSE FORMAT (JSON):
{{
  "query_type": "ui_modification|content_update|data_gathering|resume_generation|question_answer|greeting|unclear",
  "confidence": 0.95,
  "categories": ["font", "color"] or ["experience", "skills"] etc,
  "intent_description": "User wants to make name bold and change colors",
  "suggested_action": "Apply UI modifications: bold text, color changes"
}}

CLASSIFICATION RULES:
- If mixing UI and content changes, prioritize CONTENT_UPDATE
- High confidence (0.9+) for clear requests
- Medium confidence (0.7-0.9) for somewhat clear requests  
- Low confidence (0.5-0.7) for unclear requests{context_info}"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Classify this message: \"{message}\""}
        ]
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,  # type: ignore
            temperature=0.3,
            max_tokens=300
        )
        
        result_text = response.choices[0].message.content or "{}"
        
        try:
            result_data = json.loads(result_text)
            
            return QueryClassification(
                query_type=QueryType(result_data.get("query_type", "unclear")),
                confidence=float(result_data.get("confidence", 0.5)),
                categories=result_data.get("categories", []),
                intent_description=result_data.get("intent_description", ""),
                suggested_action=result_data.get("suggested_action", "")
            )
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"AI response parsing error: {e}")
            return self._fallback_classify_query(message)
    
    def _fallback_classify_query(self, message: str) -> QueryClassification:
        """Fallback pattern-based classification"""
        
        message_lower = message.lower().strip()
        
        # Score each query type
        scores = {}
        
        for query_type, patterns in self.fallback_patterns.items():
            score = sum(1 for pattern in patterns if pattern in message_lower)
            scores[query_type] = score
        
        # Find best match
        best_type = max(scores.keys(), key=lambda k: scores[k])
        max_score = scores[best_type]
        
        if max_score == 0:
            best_type = QueryType.UNCLEAR
            confidence = 0.3
        else:
            confidence = min(0.8, max_score * 0.2 + 0.5)
        
        # Determine categories based on type
        categories = []
        if best_type == QueryType.UI_MODIFICATION:
            if any(word in message_lower for word in ['color', 'blue', 'red']):
                categories.append('color')
            if any(word in message_lower for word in ['font', 'bold', 'italic']):
                categories.append('font')
            if any(word in message_lower for word in ['layout', 'compact', 'spacing']):
                categories.append('layout')
        
        return QueryClassification(
            query_type=best_type,
            confidence=confidence,
            categories=categories,
            intent_description=f"Fallback classification: {best_type.value}",
            suggested_action=f"Handle as {best_type.value}"
        )
    
    def is_ui_only_request(self, classification: QueryClassification) -> bool:
        """Check if request is UI-only modification"""
        return (
            classification.query_type == QueryType.UI_MODIFICATION and 
            classification.confidence > 0.6
        )
    
    def is_content_request(self, classification: QueryClassification) -> bool:
        """Check if request involves content changes"""
        return classification.query_type in [
            QueryType.CONTENT_UPDATE,
            QueryType.DATA_GATHERING
        ]

# Enhanced function calling system
class FunctionCallManager:
    """Manages function calls based on query classification"""
    
    def __init__(self, classifier: IntelligentQueryClassifier):
        self.classifier = classifier
        
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
        """Route query to appropriate handler based on classification"""
        
        classification = await self.classifier.classify_query(message, context)
        
        handler = self.function_map.get(classification.query_type, self._handle_unclear)
        
        return {
            "classification": classification,
            "result": await handler(message, classification, context)
        }
    
    async def _handle_ui_modification(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "ui_modification", "categories": classification.categories}
    
    async def _handle_content_update(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "content_update", "categories": classification.categories}
    
    async def _handle_data_gathering(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "data_gathering", "categories": classification.categories}
    
    async def _handle_resume_generation(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "resume_generation"}
    
    async def _handle_question_answer(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "question_answer"}
    
    async def _handle_greeting(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "greeting"}
    
    async def _handle_unclear(self, message: str, classification: QueryClassification, context: Optional[Dict]) -> Dict:
        return {"action": "clarification_needed"}

# Test the intelligent classification system
if __name__ == "__main__":
    import asyncio
    
    async def test_classification():
        classifier = IntelligentQueryClassifier()
        manager = FunctionCallManager(classifier)
        
        test_messages = [
            "make the name bold",
            "change header colors to blue", 
            "add my experience at Google",
            "I worked at Microsoft for 3 years",
            "generate my resume now",
            "hello there",
            "make headers blue and add Apple experience",
            "what information do you need?"
        ]
        
        print("🧠 Testing Intelligent Query Classification")
        print("=" * 60)
        
        for message in test_messages:
            result = await manager.route_query(message)
            classification = result["classification"]
            
            print(f"📝 Message: '{message}'")
            print(f"   Type: {classification.query_type.value}")
            print(f"   Confidence: {classification.confidence:.2f}")
            print(f"   Categories: {classification.categories}")
            print(f"   Action: {result['result']['action']}")
            print(f"   Intent: {classification.intent_description}")
            print()
        
        print("🎯 Intelligent Classification System Ready!")
        print("Features:")
        print("- AI-powered query understanding")
        print("- Fallback pattern matching")
        print("- Context-aware classification")
        print("- Smart function routing")
    
    asyncio.run(test_classification())