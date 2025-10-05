import logging
from typing import List, Dict, Any, Optional
from .text_chunker import Chunk

logger = logging.getLogger(__name__)


class ChunkAssembler:
    """Assemble processed chunks back into original format"""
    
    def __init__(self):
        self.chunk_order = []
        self.chunk_results = {}
    
    def add_chunk_result(self, chunk_id: str, result: str, metadata: Optional[Dict[str, Any]] = None):
        """Add result for a processed chunk"""
        self.chunk_results[chunk_id] = {
            'result': result,
            'metadata': metadata or {}
        }
    
    def assemble_text(self, original_chunks: List[Chunk]) -> str:
        """Assemble chunks back into complete text"""
        if not original_chunks:
            return ""
        
        # Sort chunks by start position
        sorted_chunks = sorted(original_chunks, key=lambda x: x.start_pos)
        
        assembled_parts = []
        last_end = 0
        
        for chunk in sorted_chunks:
            # Add any gap between chunks
            if chunk.start_pos > last_end:
                gap_text = " " * (chunk.start_pos - last_end)
                assembled_parts.append(gap_text)
            
            # Add chunk result if available, otherwise original text
            if chunk.chunk_id in self.chunk_results:
                result = self.chunk_results[chunk.chunk_id]['result']
                assembled_parts.append(result)
            else:
                assembled_parts.append(chunk.text)
            
            last_end = chunk.end_pos
        
        return ''.join(assembled_parts)
    
    def assemble_html(self, original_html: str, chunk_translations: Dict[str, str]) -> str:
        """Assemble HTML with translated chunks"""
        # This is a simplified version - in production you'd use proper HTML parsing
        result_html = original_html
        
        for chunk_id, translated_text in chunk_translations.items():
            # Find and replace the original text with translated text
            # This is a basic implementation - in production you'd use BeautifulSoup
            result_html = result_html.replace(chunk_id, translated_text)
        
        return result_html
    
    def get_assembly_stats(self) -> Dict[str, Any]:
        """Get statistics about chunk assembly"""
        total_chunks = len(self.chunk_results)
        successful_chunks = sum(1 for result in self.chunk_results.values() 
                               if result['result'] and result['result'].strip())
        
        return {
            'total_chunks': total_chunks,
            'successful_chunks': successful_chunks,
            'success_rate': successful_chunks / max(total_chunks, 1),
            'failed_chunks': total_chunks - successful_chunks
        }
    
    def clear_results(self):
        """Clear all chunk results"""
        self.chunk_results.clear()
        self.chunk_order.clear()
    
    def validate_assembly(self, original_chunks: List[Chunk]) -> Dict[str, Any]:
        """Validate that assembly will work correctly"""
        issues = []
        
        # Check for missing chunks
        missing_chunks = []
        for chunk in original_chunks:
            if chunk.chunk_id not in self.chunk_results:
                missing_chunks.append(chunk.chunk_id)
        
        if missing_chunks:
            issues.append(f"Missing results for {len(missing_chunks)} chunks")
        
        # Check for empty results
        empty_results = []
        for chunk_id, result in self.chunk_results.items():
            if not result['result'] or not result['result'].strip():
                empty_results.append(chunk_id)
        
        if empty_results:
            issues.append(f"Empty results for {len(empty_results)} chunks")
        
        # Check for overlapping chunks
        sorted_chunks = sorted(original_chunks, key=lambda x: x.start_pos)
        overlapping_chunks = []
        
        for i in range(len(sorted_chunks) - 1):
            current = sorted_chunks[i]
            next_chunk = sorted_chunks[i + 1]
            
            if current.end_pos > next_chunk.start_pos:
                overlapping_chunks.append((current.chunk_id, next_chunk.chunk_id))
        
        if overlapping_chunks:
            issues.append(f"Overlapping chunks detected: {len(overlapping_chunks)} pairs")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'missing_chunks': len(missing_chunks),
            'empty_results': len(empty_results),
            'overlapping_chunks': len(overlapping_chunks)
        }
    
    def optimize_assembly(self, original_chunks: List[Chunk]) -> List[Chunk]:
        """Optimize chunk order for better assembly"""
        # Sort chunks by start position
        sorted_chunks = sorted(original_chunks, key=lambda x: x.start_pos)
        
        # Remove overlapping chunks (keep the first one)
        optimized_chunks = []
        last_end = 0
        
        for chunk in sorted_chunks:
            if chunk.start_pos >= last_end:
                optimized_chunks.append(chunk)
                last_end = chunk.end_pos
            else:
                # Handle overlap by adjusting start position
                chunk.start_pos = last_end
                if chunk.start_pos < chunk.end_pos:
                    optimized_chunks.append(chunk)
                    last_end = chunk.end_pos
        
        return optimized_chunks
