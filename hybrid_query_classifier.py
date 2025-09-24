#!/usr/bin/env python3
"""
Hybrid Query Classification System - Combines speed of regex with accuracy of AI
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from intelligent_query_classifier import (
    IntelligentQueryClassifier, QueryType, QueryClassification,
    FunctionCallManager
)
import time

@dataclass 
class HybridClassificationResult:
    """Result from hybrid classification system"""
    query_type: QueryType
    confidence: float
    categories: List[str]
    intent_description: str
    method_used: str  # 'regex' or 'ai'
    processing_time_ms: float

class HybridQueryClassifier:
    """Hybrid system: Fast regex for simple patterns, AI for complex queries"""
    
    def __init__(self):
        self.ai_classifier = IntelligentQueryClassifier()
        
        # Simple, high-confidence regex patterns
        self.quick_patterns = {
            QueryType.GREETING: [
                r'\b(hello|hi|hey|good morning|good afternoon|thanks|thank you)\b',
            ],
            QueryType.UI_MODIFICATION: [
                r'\b(bold|italic|color|blue|red|larger|smaller|compact|spacing)\b.*(?!add|update|change my)',
                r'make.*\b(bold|larger|blue|compact)\b',
                r'\b(font|layout|style)\b.*(?!add|remove)'
            ],
            QueryType.CONTENT_UPDATE: [
                r'\b(add|update|change my|remove)\b.*\b(experience|skills|education|name|phone|email)\b',
                r'\b(worked at|studied at|graduated from)\b',
            ],
            QueryType.RESUME_GENERATION: [
                r'\b(generate|create|build|make)\b.*\bresume\b',
                r"\b(i'?m ready|let'?s generate)\b"
            ]
        }
        
        # AI confidence threshold - use AI for queries below this confidence
        self.ai_threshold = 0.8
        
    async def classify_query(self, message: str, context: Optional[Dict] = None) -> HybridClassificationResult:
        """Hybrid classification: regex first, AI if uncertain"""
        
        start_time = time.time()
        
        # Step 1: Try quick regex patterns
        regex_result = self._quick_regex_classify(message)
        
        if regex_result and regex_result.confidence >= self.ai_threshold:
            # High confidence regex result
            end_time = time.time()
            return HybridClassificationResult(
                query_type=regex_result.query_type,
                confidence=regex_result.confidence,
                categories=regex_result.categories,
                intent_description=f"Pattern-matched: {regex_result.intent_description}",
                method_used="regex",
                processing_time_ms=(end_time - start_time) * 1000
            )
        
        # Step 2: Use AI for complex/uncertain cases
        ai_result = await self.ai_classifier.classify_query(message, context)
        end_time = time.time()
        
        return HybridClassificationResult(
            query_type=ai_result.query_type,
            confidence=ai_result.confidence,
            categories=ai_result.categories,
            intent_description=ai_result.intent_description,
            method_used="ai",
            processing_time_ms=(end_time - start_time) * 1000
        )
    
    def _quick_regex_classify(self, message: str) -> Optional[QueryClassification]:
        """Quick regex-based classification for simple patterns"""
        
        import re
        message_lower = message.lower().strip()
        
        # Simple greeting detection
        if any(greeting in message_lower for greeting in ['hello', 'hi', 'hey', 'thanks']):
            return QueryClassification(
                query_type=QueryType.GREETING,
                confidence=0.9,
                categories=[],
                intent_description="Simple greeting",
                suggested_action="respond_greeting"
            )
        
        # Simple UI modification detection  
        ui_keywords = ['bold', 'italic', 'color', 'blue', 'red', 'larger', 'smaller', 'compact', 'spacing', 'font']
        content_keywords = ['add', 'update', 'change my', 'remove', 'worked at', 'studied at']
        
        has_ui = any(keyword in message_lower for keyword in ui_keywords)
        has_content = any(keyword in message_lower for keyword in content_keywords)
        
        if has_ui and not has_content:
            categories = []
            if any(word in message_lower for word in ['bold', 'italic', 'font']):
                categories.append('font')
            if any(word in message_lower for word in ['color', 'blue', 'red']):
                categories.append('color')
            if any(word in message_lower for word in ['larger', 'smaller']):
                categories.append('size')
                
            return QueryClassification(
                query_type=QueryType.UI_MODIFICATION,
                confidence=0.85,
                categories=categories,
                intent_description="Simple UI modification",
                suggested_action="apply_ui_changes"
            )
        
        # Simple content update detection
        if has_content:
            categories = []
            if 'experience' in message_lower or 'worked' in message_lower:
                categories.append('experience')
            if 'skills' in message_lower:
                categories.append('skills')
            if 'education' in message_lower or 'studied' in message_lower:
                categories.append('education')
                
            return QueryClassification(
                query_type=QueryType.CONTENT_UPDATE if any(word in message_lower for word in ['add', 'update', 'change', 'remove']) else QueryType.DATA_GATHERING,
                confidence=0.82,
                categories=categories,
                intent_description="Simple content modification",
                suggested_action="update_content"
            )
        
        # Resume generation detection
        if any(phrase in message_lower for phrase in ['generate resume', 'create resume', 'build resume', 'ready']):
            return QueryClassification(
                query_type=QueryType.RESUME_GENERATION,
                confidence=0.85,
                categories=[],
                intent_description="Resume generation request",
                suggested_action="generate_resume"
            )
        
        # Return None if no clear pattern matches
        return None

class OptimizedFunctionCallManager:
    """Enhanced function call manager with hybrid classification"""
    
    def __init__(self):
        self.hybrid_classifier = HybridQueryClassifier()
        
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
        """Route query using hybrid classification"""
        
        classification = await self.hybrid_classifier.classify_query(message, context)
        
        # Log performance metrics
        print(f"🚀 Query classified via {classification.method_used.upper()} in {classification.processing_time_ms:.1f}ms")
        
        handler = self.function_map.get(classification.query_type, self._handle_unclear)
        
        return {
            "classification": classification,
            "result": await handler(message, classification, context),
            "performance": {
                "method": classification.method_used,
                "time_ms": classification.processing_time_ms,
                "confidence": classification.confidence
            }
        }
    
    # Handler methods (same as before)
    async def _handle_ui_modification(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "ui_modification", "categories": classification.categories}
    
    async def _handle_content_update(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "content_update", "categories": classification.categories}
    
    async def _handle_data_gathering(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "data_gathering", "categories": classification.categories}
    
    async def _handle_resume_generation(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "resume_generation"}
    
    async def _handle_question_answer(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "question_answer"}
    
    async def _handle_greeting(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "greeting"}
    
    async def _handle_unclear(self, message: str, classification: HybridClassificationResult, context: Optional[Dict]) -> Dict:
        return {"action": "clarification_needed"}

# Test the hybrid system
if __name__ == "__main__":
    async def test_hybrid_system():
        manager = OptimizedFunctionCallManager()
        
        test_messages = [
            # Should use REGEX (simple patterns)
            "hello there",
            "make it bold",
            "change color to blue",
            "add my experience",
            "generate resume",
            
            # Should use AI (complex patterns)
            "I want to make the headers more professional looking with navy blue colors",
            "make headers blue and add my Apple internship experience", 
            "I worked as a Senior Data Scientist at Microsoft for 3 years and also freelanced",
            "the text looks too small can you make it bigger please",
            "what happens if I change my email address after generating the resume?"
        ]
        
        print("⚡ Testing Hybrid Classification System")
        print("=" * 70)
        
        total_time = 0
        regex_count = 0
        ai_count = 0
        
        for message in test_messages:
            result = await manager.route_query(message)
            classification = result["classification"]
            performance = result["performance"]
            
            total_time += performance["time_ms"]
            if performance["method"] == "regex":
                regex_count += 1
            else:
                ai_count += 1
            
            print(f"📝 {message[:50]}{'...' if len(message) > 50 else ''}")
            print(f"   Method: {performance['method'].upper():>5} | Time: {performance['time_ms']:>6.1f}ms | Type: {classification.query_type.value}")
            print(f"   Confidence: {classification.confidence:.2f} | Categories: {classification.categories}")
            print()
        
        avg_time = total_time / len(test_messages)
        
        print("📊 HYBRID SYSTEM PERFORMANCE")
        print("=" * 70)
        print(f"🚀 Average processing time: {avg_time:.1f}ms")
        print(f"⚡ Regex classifications: {regex_count}/{len(test_messages)} ({regex_count/len(test_messages)*100:.1f}%)")
        print(f"🧠 AI classifications: {ai_count}/{len(test_messages)} ({ai_count/len(test_messages)*100:.1f}%)")
        print()
        print("✅ Benefits:")
        print("   - Fast processing for simple queries") 
        print("   - High accuracy for complex queries")
        print("   - Optimal resource usage")
        print("   - Fallback reliability")
    
    asyncio.run(test_hybrid_system())