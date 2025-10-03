"""
RAG Retrieve Module - Hybrid retrieval system with BM25 and vector search
"""

from typing import List, Dict, Any, Optional, Tuple
import numpy as np
from datetime import datetime
import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

class Retriever(ABC):
    """Abstract base class for retrievers."""
    
    @abstractmethod
    def search(self, query: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        pass

class BM25Retriever(Retriever):
    """BM25-based retriever for keyword matching."""
    
    def __init__(self, documents: List[Dict[str, Any]]):
        self.documents = documents
        self.k1 = 1.2
        self.b = 0.75
        self._build_index()
    
    def _build_index(self):
        """Build BM25 index."""
        self.doc_freqs = {}
        self.idf = {}
        self.doc_len = []
        self.avg_doc_len = 0
        
        # Collect all terms
        all_terms = set()
        for doc in self.documents:
            terms = self._tokenize(doc.get('chunk_text', ''))
            all_terms.update(terms)
            self.doc_len.append(len(terms))
        
        self.avg_doc_len = np.mean(self.doc_len) if self.doc_len else 0
        
        # Calculate document frequencies
        for doc_idx, doc in enumerate(self.documents):
            terms = self._tokenize(doc.get('chunk_text', ''))
            term_counts = {}
            
            for term in terms:
                term_counts[term] = term_counts.get(term, 0) + 1
                if term not in self.doc_freqs:
                    self.doc_freqs[term] = 0
                if term_counts[term] == 1:
                    self.doc_freqs[term] += 1
            
            # Store term counts for this document
            doc['term_counts'] = term_counts
        
        # Calculate IDF
        N = len(self.documents)
        for term, df in self.doc_freqs.items():
            self.idf[term] = np.log((N - df + 0.5) / (df + 0.5))
    
    def _tokenize(self, text: str) -> List[str]:
        """Simple tokenization."""
        import re
        return re.findall(r'\b\w+\b', text.lower())
    
    def search(self, query: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search using BM25."""
        query_terms = self._tokenize(query)
        scores = []
        
        for doc_idx, doc in enumerate(self.documents):
            # Apply filters
            if filters and not self._matches_filters(doc, filters):
                continue
            
            score = self._bm25_score(query_terms, doc, doc_idx)
            scores.append((score, doc))
        
        # Sort by score and return top k
        scores.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scores[:k]]
    
    def _bm25_score(self, query_terms: List[str], doc: Dict[str, Any], doc_idx: int) -> float:
        """Calculate BM25 score for a document."""
        score = 0
        term_counts = doc.get('term_counts', {})
        doc_length = self.doc_len[doc_idx]
        
        for term in query_terms:
            if term in term_counts:
                tf = term_counts[term]
                idf = self.idf.get(term, 0)
                
                # BM25 formula
                numerator = tf * (self.k1 + 1)
                denominator = tf + self.k1 * (1 - self.b + self.b * (doc_length / self.avg_doc_len))
                
                score += idf * (numerator / denominator)
        
        return score
    
    def _matches_filters(self, doc: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if document matches filters."""
        for key, value in filters.items():
            if key in doc:
                if isinstance(value, list):
                    if doc[key] not in value:
                        return False
                else:
                    if doc[key] != value:
                        return False
        return True

class VectorRetriever(Retriever):
    """Vector-based retriever using embeddings."""
    
    def __init__(self, documents: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None):
        self.documents = documents
        self.embeddings = embeddings
        self.embedding_model = None
    
    def set_embeddings(self, embeddings: np.ndarray):
        """Set pre-computed embeddings."""
        self.embeddings = embeddings
    
    def set_embedding_model(self, model):
        """Set embedding model for computing embeddings."""
        self.embedding_model = model
    
    def search(self, query: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search using vector similarity."""
        if self.embeddings is None:
            logger.warning("No embeddings available for vector search")
            return []
        
        # Get query embedding
        query_embedding = self._get_query_embedding(query)
        if query_embedding is None:
            return []
        
        # Calculate similarities
        similarities = np.dot(self.embeddings, query_embedding)
        
        # Apply filters and get top k
        filtered_indices = []
        for i, doc in enumerate(self.documents):
            if not filters or self._matches_filters(doc, filters):
                filtered_indices.append(i)
        
        if not filtered_indices:
            return []
        
        # Get similarities for filtered documents
        filtered_similarities = similarities[filtered_indices]
        
        # Get top k indices
        top_k_indices = np.argsort(filtered_similarities)[::-1][:k]
        
        # Return documents with scores
        results = []
        for idx in top_k_indices:
            doc_idx = filtered_indices[idx]
            doc = self.documents[doc_idx].copy()
            doc['similarity_score'] = float(filtered_similarities[idx])
            results.append(doc)
        
        return results
    
    def _get_query_embedding(self, query: str) -> Optional[np.ndarray]:
        """Get embedding for query."""
        if self.embedding_model is None:
            # Use simple TF-IDF as fallback
            return self._tfidf_embedding(query)
        
        try:
            # Use the embedding model
            return self.embedding_model.encode(query)
        except Exception as e:
            logger.error(f"Error getting query embedding: {str(e)}")
            return None
    
    def _tfidf_embedding(self, query: str) -> Optional[np.ndarray]:
        """Simple TF-IDF embedding as fallback."""
        # This is a simplified implementation
        # In production, use proper TF-IDF vectorizer
        return np.random.random(384)  # Mock embedding
    
    def _matches_filters(self, doc: Dict[str, Any], filters: Dict[str, Any]) -> bool:
        """Check if document matches filters."""
        for key, value in filters.items():
            if key in doc:
                if isinstance(value, list):
                    if doc[key] not in value:
                        return False
                else:
                    if doc[key] != value:
                        return False
        return True

class HybridRetriever(Retriever):
    """Hybrid retriever combining BM25 and vector search."""
    
    def __init__(self, documents: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None):
        self.bm25_retriever = BM25Retriever(documents)
        self.vector_retriever = VectorRetriever(documents, embeddings)
        self.documents = documents
    
    def set_embeddings(self, embeddings: np.ndarray):
        """Set embeddings for vector retriever."""
        self.vector_retriever.set_embeddings(embeddings)
    
    def set_embedding_model(self, model):
        """Set embedding model for vector retriever."""
        self.vector_retriever.set_embedding_model(model)
    
    def search(self, query: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search using hybrid approach."""
        # Get results from both retrievers
        bm25_results = self.bm25_retriever.search(query, k * 2, filters)
        vector_results = self.vector_retriever.search(query, k * 2, filters)
        
        # Combine and deduplicate results
        combined_results = self._combine_results(bm25_results, vector_results, query)
        
        # Rerank results
        reranked_results = self._rerank_results(combined_results, query)
        
        return reranked_results[:k]
    
    def _combine_results(self, bm25_results: List[Dict[str, Any]], 
                        vector_results: List[Dict[str, Any]], 
                        query: str) -> List[Dict[str, Any]]:
        """Combine results from both retrievers."""
        # Create a dictionary to store unique results
        unique_results = {}
        
        # Add BM25 results
        for doc in bm25_results:
            doc_id = doc.get('chunk_id', id(doc))
            if doc_id not in unique_results:
                doc['bm25_score'] = doc.get('bm25_score', 0)
                doc['vector_score'] = 0
                unique_results[doc_id] = doc
        
        # Add vector results
        for doc in vector_results:
            doc_id = doc.get('chunk_id', id(doc))
            if doc_id in unique_results:
                unique_results[doc_id]['vector_score'] = doc.get('similarity_score', 0)
            else:
                doc['bm25_score'] = 0
                doc['vector_score'] = doc.get('similarity_score', 0)
                unique_results[doc_id] = doc
        
        return list(unique_results.values())
    
    def _rerank_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """Rerank results using a combination of scores."""
        for doc in results:
            bm25_score = doc.get('bm25_score', 0)
            vector_score = doc.get('vector_score', 0)
            
            # Simple combination (in production, use more sophisticated reranking)
            combined_score = 0.6 * bm25_score + 0.4 * vector_score
            
            # Add query relevance bonus
            query_terms = set(query.lower().split())
            doc_terms = set(doc.get('chunk_text', '').lower().split())
            overlap = len(query_terms.intersection(doc_terms))
            relevance_bonus = overlap / len(query_terms) if query_terms else 0
            
            doc['final_score'] = combined_score + 0.1 * relevance_bonus
        
        # Sort by final score
        results.sort(key=lambda x: x.get('final_score', 0), reverse=True)
        
        return results

class RAGSystem:
    """Main RAG system that coordinates retrieval and generation."""
    
    def __init__(self, documents: List[Dict[str, Any]], embeddings: Optional[np.ndarray] = None):
        self.documents = documents
        self.retriever = HybridRetriever(documents, embeddings)
        self.reranker = None  # Optional reranker
    
    def search(self, query: str, k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search for relevant documents."""
        try:
            results = self.retriever.search(query, k, filters)
            
            # Add attribution information
            for result in results:
                result['attribution'] = {
                    'title': result.get('title', 'Unknown'),
                    'url': result.get('file_path', ''),
                    'score': result.get('final_score', 0),
                    'chunk_id': result.get('chunk_id', 0)
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in RAG search: {str(e)}")
            return []
    
    def set_embeddings(self, embeddings: np.ndarray):
        """Set embeddings for the retriever."""
        self.retriever.set_embeddings(embeddings)
    
    def set_embedding_model(self, model):
        """Set embedding model for the retriever."""
        self.retriever.set_embedding_model(model)
