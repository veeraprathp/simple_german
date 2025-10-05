import re
import uuid
import logging
from typing import List, Dict, Any, Optional
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """Represents a text chunk with metadata"""
    text: str
    start_pos: int
    end_pos: int
    chunk_id: str
    metadata: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class TextChunker:
    """Intelligent text chunking for large documents"""
    
    def __init__(self, max_chunk_size: int = 1000, overlap: int = 100):
        self.max_chunk_size = max_chunk_size
        self.overlap = overlap
        self.sentence_pattern = re.compile(r'[.!?]+\s+')
        self.word_pattern = re.compile(r'\s+')
        
    def chunk_text(self, text: str) -> List[Chunk]:
        """Chunk text into manageable pieces"""
        if not text or not text.strip():
            return []
        
        # Split into sentences
        sentences = self._split_into_sentences(text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        start_pos = 0
        
        for sentence in sentences:
            sentence_size = len(sentence)
            
            # If adding this sentence would exceed max size, create a chunk
            if current_size + sentence_size > self.max_chunk_size and current_chunk:
                chunk_text = " ".join(current_chunk)
                chunks.append(Chunk(
                    text=chunk_text,
                    start_pos=start_pos,
                    end_pos=start_pos + len(chunk_text),
                    chunk_id=str(uuid.uuid4()),
                    metadata={
                        'sentence_count': len(current_chunk),
                        'char_count': len(chunk_text),
                        'word_count': len(chunk_text.split()),
                        'chunk_type': 'sentence_based'
                    }
                ))
                
                # Start new chunk with overlap
                overlap_sentences = self._get_overlap_sentences(current_chunk)
                current_chunk = overlap_sentences + [sentence]
                current_size = sum(len(s) for s in current_chunk)
                start_pos += len(chunk_text) - len(" ".join(overlap_sentences))
            else:
                current_chunk.append(sentence)
                current_size += sentence_size
        
        # Add remaining sentences
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append(Chunk(
                text=chunk_text,
                start_pos=start_pos,
                end_pos=start_pos + len(chunk_text),
                chunk_id=str(uuid.uuid4()),
                metadata={
                    'sentence_count': len(current_chunk),
                    'char_count': len(chunk_text),
                    'word_count': len(chunk_text.split()),
                    'chunk_type': 'sentence_based'
                }
            ))
        
        return chunks
    
    def chunk_by_words(self, text: str) -> List[Chunk]:
        """Chunk text by word count instead of sentences"""
        if not text or not text.strip():
            return []
        
        words = text.split()
        chunks = []
        start_pos = 0
        
        for i in range(0, len(words), self.max_chunk_size - self.overlap):
            chunk_words = words[i:i + self.max_chunk_size]
            chunk_text = " ".join(chunk_words)
            
            chunks.append(Chunk(
                text=chunk_text,
                start_pos=start_pos,
                end_pos=start_pos + len(chunk_text),
                chunk_id=str(uuid.uuid4()),
                metadata={
                    'word_count': len(chunk_words),
                    'char_count': len(chunk_text),
                    'chunk_type': 'word_based',
                    'word_start': i,
                    'word_end': min(i + self.max_chunk_size, len(words))
                }
            ))
            
            start_pos += len(chunk_text) + 1  # +1 for space
        
        return chunks
    
    def chunk_html(self, html: str) -> List[Chunk]:
        """Chunk HTML content while preserving structure"""
        # This is a simplified version - in production you'd use BeautifulSoup
        # For now, extract text and chunk it
        text = self._extract_text_from_html(html)
        return self.chunk_text(text)
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting - in production you'd use NLTK or spaCy
        sentences = self.sentence_pattern.split(text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # If no sentences found, split by paragraphs
        if not sentences:
            sentences = [p.strip() for p in text.split('\n\n') if p.strip()]
        
        # If still no sentences, split by lines
        if not sentences:
            sentences = [line.strip() for line in text.split('\n') if line.strip()]
        
        return sentences
    
    def _get_overlap_sentences(self, sentences: List[str]) -> List[str]:
        """Get overlap sentences for chunk continuity"""
        if len(sentences) <= 1:
            return sentences
        
        # Take last 1-2 sentences for overlap
        overlap_count = min(2, len(sentences))
        return sentences[-overlap_count:]
    
    def _extract_text_from_html(self, html: str) -> str:
        """Extract text from HTML (simplified version)"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_chunk_stats(self, chunks: List[Chunk]) -> Dict[str, Any]:
        """Get statistics about chunks"""
        if not chunks:
            return {}
        
        char_counts = [chunk.metadata.get('char_count', len(chunk.text)) for chunk in chunks]
        word_counts = [chunk.metadata.get('word_count', len(chunk.text.split())) for chunk in chunks]
        
        return {
            'total_chunks': len(chunks),
            'avg_char_count': sum(char_counts) / len(char_counts),
            'min_char_count': min(char_counts),
            'max_char_count': max(char_counts),
            'avg_word_count': sum(word_counts) / len(word_counts),
            'min_word_count': min(word_counts),
            'max_word_count': max(word_counts),
            'total_chars': sum(char_counts),
            'total_words': sum(word_counts)
        }
    
    def optimize_chunk_size(self, text: str, target_chunks: int = 5) -> int:
        """Optimize chunk size based on text length and target chunks"""
        text_length = len(text)
        optimal_size = text_length // target_chunks
        
        # Ensure it's within reasonable bounds
        optimal_size = max(500, min(optimal_size, 2000))
        
        return optimal_size
