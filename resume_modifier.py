#!/usr/bin/env python3
"""
Resume Modifier - Handles targeted modifications without full regeneration
"""

import re
from typing import Dict, List, Optional
from models import ResumeData

class ResumeModifier:
    """Handles targeted resume modifications without full regeneration"""
    
    def __init__(self):
        self.modification_patterns = {
            'font': self._modify_font,
            'color': self._modify_color,
            'layout': self._modify_layout,
            'spacing': self._modify_spacing,
            'size': self._modify_size,
            'style': self._modify_style,
            'format': self._modify_format
        }
    
    def can_handle_modification(self, user_query: str, existing_resume: Optional[str] = None) -> bool:
        """Check if this is a small modification that can be handled without full regeneration"""
        if not existing_resume:
            return False
        
        modification_keywords = [
            'font', 'color', 'size', 'style', 'spacing', 'format',
            'bold', 'italic', 'underline', 'larger', 'smaller',
            'bigger', 'compact', 'spacing', 'margins', 'layout'
        ]
        
        # Check if it's a small styling change
        query_lower = user_query.lower()
        
        # Must contain modification keywords
        has_modification_keyword = any(keyword in query_lower for keyword in modification_keywords)
        
        # Must NOT be adding/removing content (these are content changes, not style changes)
        content_change_keywords = [
            'add experience', 'add new', 'remove', 'delete', 'new job', 'new project',
            'add education', 'add skill', 'change company', 'change position',
            'add work', 'new experience'
        ]
        
        has_content_change = any(keyword in query_lower for keyword in content_change_keywords)
        
        return has_modification_keyword and not has_content_change
    
    def apply_modification(self, user_query: str, existing_resume: str) -> str:
        """Apply targeted modification to existing resume"""
        query_lower = user_query.lower()
        modified_resume = existing_resume
        
        # Detect modification type and apply
        if 'font' in query_lower or 'bold' in query_lower:
            modified_resume = self._modify_font(user_query, modified_resume)
        elif 'color' in query_lower:
            modified_resume = self._modify_color(user_query, modified_resume)
        elif 'compact' in query_lower or 'spacing' in query_lower or 'tighter' in query_lower:
            modified_resume = self._modify_spacing(user_query, modified_resume)
        elif 'layout' in query_lower:
            modified_resume = self._modify_layout(user_query, modified_resume)
        elif 'size' in query_lower:
            modified_resume = self._modify_size(user_query, modified_resume)
        elif 'style' in query_lower:
            modified_resume = self._modify_style(user_query, modified_resume)
        elif 'format' in query_lower:
            modified_resume = self._modify_format(user_query, modified_resume)
        
        return modified_resume
    
    def _modify_font(self, user_query: str, resume: str) -> str:
        """Modify font-related styling"""
        query_lower = user_query.lower()
        
        if 'name' in query_lower and ('font' in query_lower or 'bold' in query_lower):
            # Modify name header font
            # Find the name header (first # line)
            lines = resume.split('\n')
            for i, line in enumerate(lines):
                if line.startswith('# ') and not line.startswith('## '):
                    # Extract name without #
                    name = line[2:].strip()
                    
                    if 'bold' in query_lower or 'larger' in query_lower:
                        # Make name bold and larger
                        lines[i] = f"# **{name}**"
                    elif 'italic' in query_lower:
                        lines[i] = f"# *{name}*"
                    elif 'underline' in query_lower:
                        # Add underline using markdown
                        lines[i] = f"# {name}"
                        lines.insert(i + 1, "=" * len(name))
                    break
            
            return '\n'.join(lines)
        
        return resume
    
    def _modify_color(self, user_query: str, resume: str) -> str:
        """Modify color-related styling (add color annotations)"""
        query_lower = user_query.lower()
        
        if 'blue' in query_lower:
            # Add blue color annotation for headers
            resume = resume.replace('## ', '## 🔵 ')
        elif 'green' in query_lower:
            resume = resume.replace('## ', '## 🟢 ')
        elif 'red' in query_lower:
            resume = resume.replace('## ', '## 🔴 ')
        
        return resume
    
    def _modify_layout(self, user_query: str, resume: str) -> str:
        """Modify layout and structure"""
        query_lower = user_query.lower()
        
        if 'compact' in query_lower or 'shorter' in query_lower:
            # Remove extra line breaks
            resume = re.sub(r'\n\n\n+', '\n\n', resume)
            # Combine contact info on single line
            resume = self._make_contact_compact(resume)
        
        elif 'more space' in query_lower or 'spacious' in query_lower:
            # Add more spacing between sections
            resume = resume.replace('\n## ', '\n\n---\n\n## ')
        
        return resume
    
    def _modify_spacing(self, user_query: str, resume: str) -> str:
        """Modify spacing between elements"""
        query_lower = user_query.lower()
        
        if 'less space' in query_lower or 'compact' in query_lower or 'tighter' in query_lower:
            # Reduce spacing
            resume = re.sub(r'\n\n\n+', '\n\n', resume)
            # Remove empty lines between sections
            resume = re.sub(r'\n\n## ', '\n## ', resume)
        elif 'more space' in query_lower:
            # Add more spacing
            resume = resume.replace('\n\n', '\n\n\n')
        
        return resume
    
    def _modify_size(self, user_query: str, resume: str) -> str:
        """Modify text size using markdown"""
        query_lower = user_query.lower()
        
        if 'larger' in query_lower or 'bigger' in query_lower:
            if 'name' in query_lower:
                # Make name larger (add emphasis)
                resume = re.sub(r'^# (.+)$', r'# **\1**', resume, flags=re.MULTILINE)
        
        return resume
    
    def _modify_style(self, user_query: str, resume: str) -> str:
        """Modify overall style"""
        query_lower = user_query.lower()
        
        if 'professional' in query_lower:
            # Remove emojis and casual elements
            resume = re.sub(r'[📧🏠📞💼🎓⚡🚀🌟💻🔧📈🎯]', '', resume)
            resume = re.sub(r'\s+', ' ', resume)  # Clean up extra spaces
        
        elif 'modern' in query_lower or 'creative' in query_lower:
            # Add modern elements
            resume = resume.replace('## ', '## ✨ ')
        
        return resume
    
    def _modify_format(self, user_query: str, resume: str) -> str:
        """Modify format structure"""
        query_lower = user_query.lower()
        
        if 'table' in query_lower and 'education' in query_lower:
            # Convert education to table format
            resume = self._convert_education_to_table(resume)
        
        return resume
    
    def _make_contact_compact(self, resume: str) -> str:
        """Convert contact info to single line format"""
        lines = resume.split('\n')
        contact_lines = []
        contact_start = -1
        
        # Find contact information section
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith('#') and ('@' in line or 'linkedin' in line.lower() or '(' in line):
                if contact_start == -1:
                    contact_start = i
                contact_lines.append(line.strip())
            elif contact_start != -1 and line.strip() == '':
                break
        
        if contact_lines:
            # Combine contact info into single line
            combined_contact = ' | '.join(contact_lines)
            # Replace the contact section
            new_lines = lines[:contact_start] + [combined_contact] + lines[contact_start + len(contact_lines):]
            return '\n'.join(new_lines)
        
        return resume
    
    def _convert_education_to_table(self, resume: str) -> str:
        """Convert education section to table format"""
        # This is a simplified example - would need more sophisticated parsing
        education_section = re.search(r'## 🎓.*?(?=\n## |\n---|\Z)', resume, re.DOTALL)
        if education_section:
            # Replace with table format (simplified)
            table_format = """## 🎓 Education

| Degree | Institution | Year |
|--------|-------------|------|
| Bachelor of Science | University Name | 2020-2024 |
"""
            resume = resume.replace(education_section.group(), table_format)
        
        return resume
    
    def estimate_change_impact(self, user_query: str) -> str:
        """Estimate the impact level of the requested change"""
        query_lower = user_query.lower()
        
        small_changes = ['font', 'color', 'bold', 'italic', 'size', 'spacing', 'tighter', 'compact']
        medium_changes = ['layout', 'format', 'order', 'table', 'column']
        large_changes = ['add experience', 'add new', 'remove', 'delete', 'new job', 'new project', 'change company', 'change position']
        
        if any(change in query_lower for change in large_changes):
            return "large"
        elif any(change in query_lower for change in medium_changes):
            return "medium"
        elif any(change in query_lower for change in small_changes):
            return "small"
        else:
            return "unknown"