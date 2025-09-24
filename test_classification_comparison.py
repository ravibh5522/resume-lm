#!/usr/bin/env python3
"""
Compare the new intelligent classification system vs old regex-heavy approach
"""

import asyncio
import time
from intelligent_query_classifier import IntelligentQueryClassifier, FunctionCallManager
from advanced_ui_agent import AdvancedUIAgent
from agents import AIAgentOrchestrator

async def compare_classification_systems():
    """Compare intelligent classification vs regex-based detection"""
    
    print("📊 Comparing Query Detection Systems")
    print("=" * 80)
    
    # Initialize systems
    intelligent_classifier = IntelligentQueryClassifier()
    old_ui_agent = AdvancedUIAgent()
    
    # Test cases with expected results
    test_cases = [
        {
            "message": "make the name bold and larger",
            "expected_type": "ui_modification",
            "complexity": "simple"
        },
        {
            "message": "I want to change the header colors to navy blue and make the layout more professional",
            "expected_type": "ui_modification", 
            "complexity": "complex"
        },
        {
            "message": "add my software engineering experience at Google from 2020 to 2023",
            "expected_type": "content_update",
            "complexity": "simple"
        },
        {
            "message": "I worked as a Senior Data Scientist at Microsoft for 3 years and also freelanced for various startups",
            "expected_type": "data_gathering",
            "complexity": "complex"
        },
        {
            "message": "make headers blue and add my Apple internship experience",
            "expected_type": "content_update",  # Mixed request, content should win
            "complexity": "mixed"
        },
        {
            "message": "create a modern, professional layout with navy blue headers and compact spacing",
            "expected_type": "ui_modification",
            "complexity": "complex"
        },
        {
            "message": "hello, I need help building my resume",
            "expected_type": "greeting",
            "complexity": "simple"
        },
        {
            "message": "what happens if I change my email address?",
            "expected_type": "question_answer",
            "complexity": "simple"
        },
        {
            "message": "the text looks too small can you make it bigger please",
            "expected_type": "ui_modification",
            "complexity": "conversational"
        },
        {
            "message": "update my skills to include Python, React, and machine learning",
            "expected_type": "content_update",
            "complexity": "simple"
        }
    ]
    
    print("🧠 INTELLIGENT AI-POWERED CLASSIFICATION")
    print("-" * 50)
    
    intelligent_correct = 0
    intelligent_times = []
    
    for i, test in enumerate(test_cases, 1):
        message = test["message"]
        expected = test["expected_type"]
        complexity = test["complexity"]
        
        start_time = time.time()
        classification = await intelligent_classifier.classify_query(message)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
        intelligent_times.append(processing_time)
        
        detected_type = classification.query_type.value
        is_correct = detected_type == expected
        
        if is_correct:
            intelligent_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} Test {i:2d} ({complexity:>12}): {message[:50]}{'...' if len(message) > 50 else ''}")
        print(f"        Expected: {expected:>15} | Detected: {detected_type:>15} | Time: {processing_time:>5.1f}ms")
        print(f"        Confidence: {classification.confidence:.2f} | Categories: {classification.categories}")
        print()
    
    print("🔍 OLD REGEX-BASED DETECTION")  
    print("-" * 50)
    
    regex_correct = 0
    regex_times = []
    
    for i, test in enumerate(test_cases, 1):
        message = test["message"]
        expected = test["expected_type"]
        complexity = test["complexity"]
        
        start_time = time.time()
        is_ui_request = old_ui_agent.is_ui_modification_request(message)
        end_time = time.time()
        
        processing_time = (end_time - start_time) * 1000  # Convert to milliseconds
        regex_times.append(processing_time)
        
        # Map boolean result to types (simplified)
        if is_ui_request:
            detected_type = "ui_modification"
        elif any(word in message.lower() for word in ['hello', 'hi', 'thanks']):
            detected_type = "greeting"
        elif any(word in message.lower() for word in ['what', 'how', 'why']):
            detected_type = "question_answer"
        elif any(word in message.lower() for word in ['add', 'update', 'change my', 'worked at']):
            detected_type = "content_update" if not is_ui_request else "ui_modification"
        else:
            detected_type = "data_gathering"
        
        is_correct = detected_type == expected
        
        if is_correct:
            regex_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} Test {i:2d} ({complexity:>12}): {message[:50]}{'...' if len(message) > 50 else ''}")
        print(f"        Expected: {expected:>15} | Detected: {detected_type:>15} | Time: {processing_time:>5.1f}ms")
        
        categories = old_ui_agent.get_ui_modification_categories(message) if is_ui_request else []
        print(f"        Categories: {categories}")
        print()
    
    # Performance comparison
    total_tests = len(test_cases)
    intelligent_accuracy = (intelligent_correct / total_tests) * 100
    regex_accuracy = (regex_correct / total_tests) * 100
    
    avg_intelligent_time = sum(intelligent_times) / len(intelligent_times)
    avg_regex_time = sum(regex_times) / len(regex_times)
    
    print("📈 PERFORMANCE COMPARISON")
    print("=" * 80)
    
    print(f"🎯 ACCURACY:")
    print(f"   Intelligent System: {intelligent_correct}/{total_tests} ({intelligent_accuracy:.1f}%)")
    print(f"   Regex System:       {regex_correct}/{total_tests} ({regex_accuracy:.1f}%)")
    print(f"   Improvement:        +{intelligent_accuracy - regex_accuracy:.1f}%")
    print()
    
    print(f"⚡ SPEED:")
    print(f"   Intelligent System: {avg_intelligent_time:.1f}ms average")
    print(f"   Regex System:       {avg_regex_time:.1f}ms average")
    print(f"   Speed Trade-off:    {avg_intelligent_time / avg_regex_time:.1f}x slower")
    print()
    
    print("🏆 ADVANTAGES OF INTELLIGENT SYSTEM:")
    print("✅ Higher accuracy with complex/conversational queries")
    print("✅ Better context understanding")
    print("✅ Confidence scores for decision making")
    print("✅ Detailed intent descriptions")
    print("✅ Handles mixed requests intelligently")
    print("✅ Natural language understanding")
    print("✅ Reduces false positives")
    print()
    
    print("⚡ ADVANTAGES OF REGEX SYSTEM:")
    print("✅ Extremely fast processing")
    print("✅ Deterministic results")
    print("✅ No API dependencies")
    print("✅ Reliable for simple patterns")
    print()
    
    print("💡 RECOMMENDATION:")
    if intelligent_accuracy > regex_accuracy + 10:
        print("Use Intelligent System for better accuracy and user experience")
    else:
        print("Consider hybrid approach: regex for simple patterns, AI for complex queries")

async def test_real_world_scenarios():
    """Test with real-world user scenarios"""
    
    print("\n🌍 REAL-WORLD SCENARIO TESTING")
    print("=" * 80)
    
    orchestrator = AIAgentOrchestrator()
    
    scenarios = [
        {
            "scenario": "New user starting resume",
            "messages": [
                "hi there, I need help with my resume",
                "my name is Sarah Johnson and I live in New York",
                "I worked at Tesla as a software engineer for 2 years", 
                "make the headers look more professional",
                "add my education from MIT"
            ]
        },
        {
            "scenario": "User making quick styling changes", 
            "messages": [
                "make the name bigger and bold",
                "change colors to navy blue",
                "use more compact spacing"
            ]
        },
        {
            "scenario": "Mixed content and styling requests",
            "messages": [
                "change my phone number to 555-0123 and make it blue",
                "add Google internship and make headers bold",
                "update skills to Python, React and use modern styling"
            ]
        }
    ]
    
    for scenario in scenarios:
        print(f"📋 Scenario: {scenario['scenario']}")
        print("-" * 40)
        
        for i, message in enumerate(scenario['messages'], 1):
            try:
                result = await orchestrator.function_manager.route_query(message)
                classification = result["classification"]
                
                print(f"  {i}. \"{message}\"")
                print(f"     → {classification.query_type.value} ({classification.confidence:.2f})")
                print(f"     → {classification.intent_description}")
                print()
                
            except Exception as e:
                print(f"  {i}. \"{message}\" → Error: {e}")
                print()
        
        print()

if __name__ == "__main__":
    asyncio.run(compare_classification_systems())
    print("\n" + "="*80)
    asyncio.run(test_real_world_scenarios())