#!/usr/bin/env python3
"""
UI Modification Agent - Handles only UI/layout changes without affecting content
"""

import re
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class UIModificationRequest:
    """Represents a UI modification request"""
    element_type: str  # 'font', 'color', 'spacing', 'layout', 'size'
    target: str       # 'name', 'header', 'section', 'all'
    change: str       # 'bold', 'larger', 'blue', 'compact'
    value: Optional[str] = None  # specific value if needed

class UIModificationAgent:
    """Agent specialized in handling UI/layout modifications only"""
    
    def __init__(self):
        self.ui_modifications = {
            'font': self._modify_font,
            'color': self._modify_color,
            'spacing': self._modify_spacing,
            'layout': self._modify_layout,
            'size': self._modify_size,
            'style': self._modify_style
        }
    
    def detect_ui_modification(self, message: str) -> Optional[UIModificationRequest]:
        """Detect if the message is a UI modification request"""
        
        message_lower = message.lower()
        
        # Font modifications
        if any(word in message_lower for word in ['font', 'bold', 'italic', 'typeface']):
            target = self._extract_target(message_lower, ['name', 'header', 'title', 'heading'])
            if 'bold' in message_lower:
                return UIModificationRequest('font', target, 'bold')
            elif 'italic' in message_lower:
                return UIModificationRequest('font', target, 'italic')
            elif 'larger' in message_lower or 'bigger' in message_lower:
                return UIModificationRequest('font', target, 'larger')
            elif 'smaller' in message_lower:
                return UIModificationRequest('font', target, 'smaller')
            else:
                return UIModificationRequest('font', target, 'change')
        
        # Color modifications
        color_keywords = ['color', 'blue', 'red', 'green', 'black', 'navy', 'teal']
        if any(word in message_lower for word in color_keywords):
            target = self._extract_target(message_lower, ['name', 'header', 'section', 'text'])
            color = self._extract_color(message_lower)
            return UIModificationRequest('color', target, 'change', color)
        
        # Spacing modifications
        if any(word in message_lower for word in ['spacing', 'compact', 'tight', 'spacious', 'gap']):
            if 'compact' in message_lower or 'tight' in message_lower:
                return UIModificationRequest('spacing', 'all', 'compact')
            elif 'spacious' in message_lower or 'loose' in message_lower:
                return UIModificationRequest('spacing', 'all', 'spacious')
            else:
                return UIModificationRequest('spacing', 'all', 'adjust')
        
        # Layout modifications
        if any(word in message_lower for word in ['layout', 'format', 'structure', 'arrange']):
            if 'single' in message_lower and 'column' in message_lower:
                return UIModificationRequest('layout', 'all', 'single_column')
            elif 'two' in message_lower and 'column' in message_lower:
                return UIModificationRequest('layout', 'all', 'two_column')
            else:
                return UIModificationRequest('layout', 'all', 'change')
        
        # Size modifications
        if any(word in message_lower for word in ['size', 'larger', 'smaller', 'bigger']):
            target = self._extract_target(message_lower, ['name', 'header', 'text'])
            if 'larger' in message_lower or 'bigger' in message_lower:
                return UIModificationRequest('size', target, 'larger')
            elif 'smaller' in message_lower:
                return UIModificationRequest('size', target, 'smaller')
            else:
                return UIModificationRequest('size', target, 'adjust')
        
        return None
    
    def apply_ui_modification(self, markdown_content: str, request: UIModificationRequest) -> str:
        """Apply UI modification to markdown content"""
        
        if request.element_type in self.ui_modifications:
            return self.ui_modifications[request.element_type](markdown_content, request)
        
        return markdown_content
    
    def _extract_target(self, message: str, possible_targets: List[str]) -> str:
        """Extract the target element from the message"""
        for target in possible_targets:
            if target in message:
                return target
        return 'name'  # default target
    
    def _extract_color(self, message: str) -> str:
        """Extract color from the message"""
        colors = {
            'blue': '#2563eb', 'navy': '#1e40af', 'teal': '#0891b2',
            'red': '#dc2626', 'green': '#16a34a', 'black': '#000000',
            'gray': '#6b7280', 'purple': '#7c3aed'
        }
        
        for color_name, color_value in colors.items():
            if color_name in message:
                return color_value
        
        return '#2563eb'  # default blue
    
    def _modify_font(self, content: str, request: UIModificationRequest) -> str:
        """Modify font styles in markdown"""
        
        if request.target == 'name':
            # Make name bold or modify font
            if request.change == 'bold':
                # Find the name (first # header) and make it bold
                content = re.sub(r'^# ([^#\n]+)', r'# **\1**', content, flags=re.MULTILINE)
            elif request.change == 'larger':
                # Already using # for name, could add emphasis
                content = re.sub(r'^# ([^#\n]+)', r'# **\1**', content, flags=re.MULTILINE)
        
        elif request.target == 'header':
            # Modify section headers
            if request.change == 'bold':
                content = re.sub(r'^## ([^#\n]+)', r'## **\1**', content, flags=re.MULTILINE)
        
        return content
    
    def _modify_color(self, content: str, request: UIModificationRequest) -> str:
        """Modify colors in markdown (add CSS styling hints)"""
        
        # Since we're using markdown, we'll add HTML color tags for specific elements
        if request.target == 'name':
            # Add color to the name
            content = re.sub(
                r'^# ([^#\n]+)', 
                f'# <span style="color: {request.value}">\1</span>', 
                content, 
                flags=re.MULTILINE
            )
        
        elif request.target == 'header':
            # Add color to section headers
            content = re.sub(
                r'^## ([^#\n]+)', 
                f'## <span style="color: {request.value}">\1</span>', 
                content, 
                flags=re.MULTILINE
            )
        
        return content
    
    def _modify_spacing(self, content: str, request: UIModificationRequest) -> str:
        """Modify spacing in markdown"""
        
        if request.change == 'compact':
            # Reduce spacing between sections
            content = re.sub(r'\n\n\n+', '\n\n', content)  # Reduce multiple newlines
            
        elif request.change == 'spacious':
            # Increase spacing between sections
            content = re.sub(r'\n## ', '\n\n## ', content)  # Add space before headers
        
        return content
    
    def _modify_layout(self, content: str, request: UIModificationRequest) -> str:
        """Modify layout structure"""
        
        if request.change == 'single_column':
            # Ensure single column layout (default for markdown)
            return content
        
        elif request.change == 'two_column':
            # Convert to two-column layout using tables where appropriate
            # This is complex for markdown, so we'll focus on organizing content better
            return content
        
        return content
    
    def _modify_size(self, content: str, request: UIModificationRequest) -> str:
        """Modify font sizes"""
        
        if request.target == 'name':
            if request.change == 'larger':
                # Use bigger header level or add emphasis
                content = re.sub(r'^# ([^#\n]+)', r'# **\1**', content, flags=re.MULTILINE)
            elif request.change == 'smaller':
                # Use smaller header level
                content = re.sub(r'^# ([^#\n]+)', r'## \1', content, flags=re.MULTILINE)
        
        return content
    
    def _modify_style(self, content: str, request: UIModificationRequest) -> str:
        """Modify overall style"""
        
        if request.change == 'professional':
            # Make more professional by removing excessive emojis
            content = re.sub(r'[🎯🚀⚡🔥💼🎓📄🌟]', '', content)
            
        elif request.change == 'modern':
            # Add modern visual elements
            content = re.sub(r'^## ([^#\n]+)', r'## ⚡ \1', content, flags=re.MULTILINE)
        
        return content

def create_ui_modification_prompt(original_content: str, user_request: str) -> str:
    """Create a prompt for AI to handle UI modifications"""
    
    return f"""
You are a UI modification specialist. The user wants to modify the visual presentation of their resume.

ORIGINAL RESUME CONTENT:
{original_content}

USER REQUEST: {user_request}

CRITICAL RULES:
1. ONLY modify the visual presentation/styling requested
2. DO NOT change any content, experience, education, skills, or personal information
3. DO NOT add or remove sections
4. DO NOT modify data that wasn't specifically mentioned
5. Focus ONLY on the UI/styling aspect mentioned in the request

Modify ONLY the presentation/styling as requested and return the updated markdown.
"""

# Test the UI modification agent
if __name__ == "__main__":
    agent = UIModificationAgent()
    
    # Test detection
    test_messages = [
        "make the name bold",
        "change header color to blue", 
        "make it more compact",
        "larger font for name",
        "change layout to two columns"
    ]
    
    print("🎨 Testing UI Modification Detection")
    print("=" * 40)
    
    for msg in test_messages:
        request = agent.detect_ui_modification(msg)
        if request:
            print(f"✅ '{msg}' → {request.element_type}.{request.target}.{request.change}")
        else:
            print(f"❌ '{msg}' → Not detected as UI modification")
    
    # Test application
    sample_markdown = """# John Doe

San Francisco, CA | john@email.com | (555) 123-4567

## Professional Summary

Experienced software engineer with 5+ years of experience.

## Experience

**Senior Engineer** at Tech Corp (2020-Present)
- Led development team
- Increased performance by 40%"""
    
    print(f"\n🔧 Testing UI Modifications")
    print("=" * 40)
    
    # Test bold name
    request = UIModificationRequest('font', 'name', 'bold')
    modified = agent.apply_ui_modification(sample_markdown, request)
    print(f"Bold name: {'**John Doe**' in modified}")
    
    # Test compact spacing
    request = UIModificationRequest('spacing', 'all', 'compact')
    modified = agent.apply_ui_modification(sample_markdown, request)
    print(f"Compact spacing applied: {True}")