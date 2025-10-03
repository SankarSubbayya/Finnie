"""
RAG Ingest Module - Processes and chunks educational content
"""

from typing import List, Dict, Any, Optional
import os
import json
import hashlib
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ContentIngester:
    """Handles ingestion and processing of educational content."""
    
    def __init__(self, chunk_size: int = 512, overlap: int = 100):
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.supported_formats = ['.md', '.txt', '.pdf', '.html']
    
    def ingest_directory(self, directory_path: str) -> List[Dict[str, Any]]:
        """Ingest all supported files from a directory."""
        chunks = []
        directory = Path(directory_path)
        
        if not directory.exists():
            logger.error(f"Directory {directory_path} does not exist")
            return chunks
        
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.supported_formats:
                try:
                    file_chunks = self.ingest_file(str(file_path))
                    chunks.extend(file_chunks)
                    logger.info(f"Ingested {len(file_chunks)} chunks from {file_path}")
                except Exception as e:
                    logger.error(f"Error ingesting {file_path}: {str(e)}")
        
        return chunks
    
    def ingest_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Ingest a single file and return chunks."""
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"File {file_path} does not exist")
            return []
        
        # Read file content
        content = self._read_file(file_path)
        if not content:
            return []
        
        # Extract metadata
        metadata = self._extract_metadata(file_path, content)
        
        # Chunk the content
        chunks = self._chunk_content(content, metadata)
        
        return chunks
    
    def _read_file(self, file_path: Path) -> str:
        """Read file content based on file type."""
        try:
            if file_path.suffix.lower() == '.md':
                return file_path.read_text(encoding='utf-8')
            elif file_path.suffix.lower() == '.txt':
                return file_path.read_text(encoding='utf-8')
            elif file_path.suffix.lower() == '.html':
                return self._extract_text_from_html(file_path)
            elif file_path.suffix.lower() == '.pdf':
                return self._extract_text_from_pdf(file_path)
            else:
                logger.warning(f"Unsupported file type: {file_path.suffix}")
                return ""
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return ""
    
    def _extract_text_from_html(self, file_path: Path) -> str:
        """Extract text content from HTML file."""
        try:
            from bs4 import BeautifulSoup
            with open(file_path, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                return soup.get_text()
        except ImportError:
            logger.warning("BeautifulSoup not available, using basic text extraction")
            return file_path.read_text(encoding='utf-8')
        except Exception as e:
            logger.error(f"Error extracting text from HTML {file_path}: {str(e)}")
            return ""
    
    def _extract_text_from_pdf(self, file_path: Path) -> str:
        """Extract text content from PDF file."""
        try:
            import PyPDF2
            with open(file_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            logger.warning("PyPDF2 not available, cannot extract PDF text")
            return ""
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            return ""
    
    def _extract_metadata(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Extract metadata from file."""
        metadata = {
            "file_path": str(file_path),
            "file_name": file_path.name,
            "file_type": file_path.suffix.lower(),
            "file_size": file_path.stat().st_size,
            "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
            "content_hash": hashlib.md5(content.encode()).hexdigest()
        }
        
        # Extract title from content
        title = self._extract_title(content, file_path)
        if title:
            metadata["title"] = title
        
        # Extract level from file path or content
        level = self._extract_level(file_path, content)
        if level:
            metadata["level"] = level
        
        # Extract topics from content
        topics = self._extract_topics(content)
        if topics:
            metadata["topics"] = topics
        
        return metadata
    
    def _extract_title(self, content: str, file_path: Path) -> Optional[str]:
        """Extract title from content."""
        lines = content.split('\n')
        
        # Look for markdown title
        for line in lines[:10]:  # Check first 10 lines
            if line.startswith('# '):
                return line[2:].strip()
            elif line.startswith('## '):
                return line[3:].strip()
        
        # Use filename as fallback
        return file_path.stem.replace('_', ' ').replace('-', ' ').title()
    
    def _extract_level(self, file_path: Path, content: str) -> Optional[str]:
        """Extract difficulty level from file path or content."""
        # Check file path for level indicators
        path_parts = str(file_path).lower().split('/')
        for part in path_parts:
            if part in ['beginner', 'intermediate', 'advanced']:
                return part
        
        # Check content for level indicators
        content_lower = content.lower()
        if 'beginner' in content_lower or 'basic' in content_lower:
            return 'beginner'
        elif 'intermediate' in content_lower or 'moderate' in content_lower:
            return 'intermediate'
        elif 'advanced' in content_lower or 'expert' in content_lower:
            return 'advanced'
        
        return None
    
    def _extract_topics(self, content: str) -> List[str]:
        """Extract topics from content."""
        # Simple keyword extraction (in production, use NLP)
        financial_topics = [
            'portfolio', 'risk', 'return', 'diversification', 'volatility',
            'sharpe ratio', 'beta', 'alpha', 'correlation', 'covariance',
            'efficient frontier', 'capm', 'arbitrage', 'options', 'derivatives',
            'bonds', 'stocks', 'etfs', 'mutual funds', 'rebalancing'
        ]
        
        topics = []
        content_lower = content.lower()
        
        for topic in financial_topics:
            if topic in content_lower:
                topics.append(topic)
        
        return topics[:10]  # Limit to top 10 topics
    
    def _chunk_content(self, content: str, metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Chunk content into smaller pieces."""
        chunks = []
        
        # Split content into sentences
        sentences = self._split_into_sentences(content)
        
        # Create chunks with overlap
        current_chunk = []
        current_length = 0
        
        for sentence in sentences:
            sentence_length = len(sentence.split())
            
            # If adding this sentence would exceed chunk size, save current chunk
            if current_length + sentence_length > self.chunk_size and current_chunk:
                chunk_text = ' '.join(current_chunk)
                chunk_metadata = metadata.copy()
                chunk_metadata.update({
                    "chunk_id": len(chunks),
                    "chunk_text": chunk_text,
                    "chunk_length": len(chunk_text.split()),
                    "start_sentence": len(chunks) * (self.chunk_size - self.overlap),
                    "end_sentence": len(chunks) * (self.chunk_size - self.overlap) + len(current_chunk)
                })
                chunks.append(chunk_metadata)
                
                # Start new chunk with overlap
                overlap_sentences = current_chunk[-self.overlap:] if len(current_chunk) >= self.overlap else current_chunk
                current_chunk = overlap_sentences + [sentence]
                current_length = sum(len(s.split()) for s in current_chunk)
            else:
                current_chunk.append(sentence)
                current_length += sentence_length
        
        # Add final chunk
        if current_chunk:
            chunk_text = ' '.join(current_chunk)
            chunk_metadata = metadata.copy()
            chunk_metadata.update({
                "chunk_id": len(chunks),
                "chunk_text": chunk_text,
                "chunk_length": len(chunk_text.split()),
                "start_sentence": len(chunks) * (self.chunk_size - self.overlap),
                "end_sentence": len(chunks) * (self.chunk_size - self.overlap) + len(current_chunk)
            })
            chunks.append(chunk_metadata)
        
        return chunks
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        import re
        
        # Simple sentence splitting (in production, use spaCy or NLTK)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_path: str):
        """Save chunks to a JSON file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(chunks)} chunks to {output_path}")
        except Exception as e:
            logger.error(f"Error saving chunks to {output_path}: {str(e)}")
    
    def load_chunks(self, input_path: str) -> List[Dict[str, Any]]:
        """Load chunks from a JSON file."""
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            logger.info(f"Loaded {len(chunks)} chunks from {input_path}")
            return chunks
        except Exception as e:
            logger.error(f"Error loading chunks from {input_path}: {str(e)}")
            return []
