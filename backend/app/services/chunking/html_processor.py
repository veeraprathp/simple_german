import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class TextNode:
    """Represents a text node in HTML"""
    element: str
    text: str
    xpath: str
    css_selector: str
    node_id: str
    attributes: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.attributes is None:
            self.attributes = {}


class HTMLProcessor:
    """HTML parsing and text extraction for web content"""
    
    def __init__(self):
        self.text_elements = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'span', 'div', 'li', 'td', 'th']
        self.ignore_elements = ['script', 'style', 'nav', 'footer', 'header', 'aside']
    
    def extract_text_nodes(self, html: str) -> List[TextNode]:
        """Extract text nodes from HTML"""
        nodes = []
        
        # Simple HTML parsing - in production you'd use BeautifulSoup
        # For now, use regex to extract text from common elements
        
        for element in self.text_elements:
            pattern = f'<{element}[^>]*>(.*?)</{element}>'
            matches = re.finditer(pattern, html, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                text = self._clean_text(match.group(1))
                if text and len(text.strip()) > 0:
                    nodes.append(TextNode(
                        element=element,
                        text=text,
                        xpath=self._generate_xpath(element, match.start()),
                        css_selector=self._generate_css_selector(element),
                        node_id=str(uuid.uuid4()),
                        attributes=self._extract_attributes(match.group(0))
                    ))
        
        return nodes
    
    def extract_main_content(self, html: str) -> str:
        """Extract main content from HTML, removing navigation, ads, etc."""
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Remove navigation elements
        html = re.sub(r'<nav[^>]*>.*?</nav>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<header[^>]*>.*?</header>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<footer[^>]*>.*?</footer>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<aside[^>]*>.*?</aside>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Extract text from main content elements
        main_elements = ['main', 'article', 'section', 'div']
        text_parts = []
        
        for element in main_elements:
            pattern = f'<{element}[^>]*>(.*?)</{element}>'
            matches = re.finditer(pattern, html, re.DOTALL | re.IGNORECASE)
            
            for match in matches:
                text = self._clean_text(match.group(1))
                if text and len(text.strip()) > 50:  # Only substantial content
                    text_parts.append(text)
        
        return '\n\n'.join(text_parts)
    
    def reconstruct_html(self, original_html: str, translations: Dict[str, str]) -> str:
        """Reconstruct HTML with translated text"""
        result_html = original_html
        
        for xpath, translated_text in translations.items():
            # Find the element by xpath and replace its content
            # This is simplified - in production you'd use proper XPath parsing
            pattern = r'<([^>]+)>([^<]*)</\1>'
            
            def replace_content(match):
                tag = match.group(1)
                original_text = match.group(2)
                
                if original_text.strip() in translations.values():
                    return f'<{tag}>{translated_text}</{tag}>'
                return match.group(0)
            
            result_html = re.sub(pattern, replace_content, result_html)
        
        return result_html
    
    def get_text_statistics(self, html: str) -> Dict[str, Any]:
        """Get statistics about text content in HTML"""
        text_nodes = self.extract_text_nodes(html)
        
        if not text_nodes:
            return {
                'total_nodes': 0,
                'total_text_length': 0,
                'avg_text_length': 0,
                'element_distribution': {}
            }
        
        total_length = sum(len(node.text) for node in text_nodes)
        element_counts = {}
        
        for node in text_nodes:
            element_counts[node.element] = element_counts.get(node.element, 0) + 1
        
        return {
            'total_nodes': len(text_nodes),
            'total_text_length': total_length,
            'avg_text_length': total_length / len(text_nodes),
            'element_distribution': element_counts,
            'longest_text': max((node.text for node in text_nodes), key=len) if text_nodes else "",
            'shortest_text': min((node.text for node in text_nodes), key=len) if text_nodes else ""
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove HTML entities
        text = re.sub(r'&[^;]+;', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def _generate_xpath(self, element: str, position: int) -> str:
        """Generate XPath for element (simplified)"""
        return f"//{element}[{position}]"
    
    def _generate_css_selector(self, element: str) -> str:
        """Generate CSS selector for element"""
        return element
    
    def _extract_attributes(self, html_tag: str) -> Dict[str, str]:
        """Extract attributes from HTML tag"""
        attributes = {}
        
        # Simple attribute extraction
        attr_pattern = r'(\w+)="([^"]*)"'
        matches = re.finditer(attr_pattern, html_tag)
        
        for match in matches:
            attributes[match.group(1)] = match.group(2)
        
        return attributes
    
    def is_meaningful_content(self, text: str) -> bool:
        """Check if text contains meaningful content"""
        if not text or len(text.strip()) < 10:
            return False
        
        # Check for common non-content patterns
        non_content_patterns = [
            r'^\s*$',  # Empty or whitespace only
            r'^\d+$',  # Numbers only
            r'^[^\w\s]+$',  # Special characters only
            r'^(click|read more|continue|next|previous)$',  # Navigation text
        ]
        
        for pattern in non_content_patterns:
            if re.match(pattern, text, re.IGNORECASE):
                return False
        
        return True
