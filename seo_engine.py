"""
SEO Analysis Engine for Saveetha Institute
Implements TF-IDF, Cosine Similarity, and Evaluation Metrics (Precision, Recall, F1-Score)
"""

import numpy as np
from typing import List, Dict, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics.pairwise import cosine_similarity
import json


class SEOEngine:
    """
    Core SEO Analysis Engine using TF-IDF vectorization and similarity metrics.
    Evaluates search relevance and provides optimization recommendations.
    """

    def __init__(self, corpus: List[str]):
        """
        Initialize the SEO Engine with a corpus of documents.
        
        Args:
            corpus: List of text documents to build TF-IDF matrix
        """
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        self.corpus = corpus
        self.tfidf_matrix = self.vectorizer.fit_transform(corpus)
        self.feature_names = self.vectorizer.get_feature_names_out()

    def evaluate_relevance(self, query: str, page_text: str) -> float:
        """
        Calculate cosine similarity between query and page text.
        
        Args:
            query: Search query text
            page_text: Website page content
            
        Returns:
            Relevance score (0-1)
        """
        try:
            query_vec = self.vectorizer.transform([query])
            page_vec = self.vectorizer.transform([page_text])
            similarity = cosine_similarity(query_vec, page_vec)[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Error evaluating relevance: {e}")
            return 0.0

    def calculate_metrics(self, ground_truth: List[int], predictions: List[int]) -> Dict[str, float]:
        """
        Calculate Precision, Recall, and F1-Score.
        
        Args:
            ground_truth: Ground truth binary labels
            predictions: Predicted binary labels
            
        Returns:
            Dictionary with precision, recall, and f1_score
        """
        try:
            precision = precision_score(ground_truth, predictions, average='binary', zero_division=0)
            recall = recall_score(ground_truth, predictions, average='binary', zero_division=0)
            f1 = f1_score(ground_truth, predictions, average='binary', zero_division=0)
            return {
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1)
            }
        except Exception as e:
            print(f"Error calculating metrics: {e}")
            return {"precision": 0.0, "recall": 0.0, "f1_score": 0.0}

    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """
        Extract top TF-IDF keywords from text.
        
        Args:
            text: Input text
            top_n: Number of top keywords to return
            
        Returns:
            List of (keyword, score) tuples
        """
        try:
            text_vec = self.vectorizer.transform([text])
            feature_scores = text_vec.toarray()[0]
            top_indices = np.argsort(feature_scores)[-top_n:][::-1]
            
            keywords = []
            for idx in top_indices:
                if feature_scores[idx] > 0:
                    keywords.append((self.feature_names[idx], float(feature_scores[idx])))
            return keywords
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []

    def recommend_meta_tags(self, title: str, content: str, top_n: int = 5) -> Dict[str, any]:
        """
        Generate SEO recommendations for meta tags and title optimization.
        
        Args:
            title: Current page title
            content: Page content
            top_n: Number of top keywords for recommendations
            
        Returns:
            Dictionary with optimization recommendations
        """
        keywords = self.extract_keywords(content, top_n)
        keyword_list = [kw[0] for kw in keywords]
        
        recommendations = {
            "optimized_title": self._optimize_title(title, keyword_list),
            "meta_description": self._generate_meta_description(content, keyword_list),
            "recommended_keywords": keyword_list,
            "keyword_scores": {kw[0]: kw[1] for kw in keywords}
        }
        return recommendations

    def _optimize_title(self, current_title: str, keywords: List[str]) -> str:
        """Generate optimized title with keywords."""
        if keywords:
            primary_keyword = keywords[0]
            if len(current_title) < 60:
                return f"{current_title} | {primary_keyword.title()}"
            return current_title
        return current_title

    def _generate_meta_description(self, content: str, keywords: List[str]) -> str:
        """Generate optimized meta description."""
        words = content.split()[:30]
        description = ' '.join(words)
        if len(description) > 160:
            description = description[:157] + "..."
        return description

    def analyze_sitemaps(self, urls: List[str]) -> Dict[str, any]:
        """
        Analyze multiple URLs for SEO quality.
        
        Args:
            urls: List of URLs to analyze
            
        Returns:
            Analysis results for each URL
        """
        results = []
        for url in urls:
            results.append({
                "url": url,
                "analysis_status": "pending",
                "seo_score": 0.0
            })
        return {"analysis": results}

    def calculate_page_quality_score(self, 
                                    title_length: int,
                                    description_length: int,
                                    keyword_density: float,
                                    anchor_text_count: int) -> float:
        """
        Calculate overall page quality score (0-100).
        
        Args:
            title_length: Length of page title
            description_length: Length of meta description
            keyword_density: Density of keywords in content
            anchor_text_count: Number of internal links
            
        Returns:
            Quality score (0-100)
        """
        score = 0.0
        
        # Title optimization (0-25)
        if 30 <= title_length <= 60:
            score += 25
        elif 20 <= title_length <= 70:
            score += 15
        else:
            score += 5
        
        # Meta description (0-25)
        if 120 <= description_length <= 160:
            score += 25
        elif 100 <= description_length <= 170:
            score += 15
        else:
            score += 5
        
        # Keyword density (0-25)
        if 1.0 <= keyword_density <= 3.0:
            score += 25
        elif 0.5 <= keyword_density <= 4.0:
            score += 15
        else:
            score += 5
        
        # Internal links (0-25)
        if anchor_text_count >= 5:
            score += 25
        elif anchor_text_count >= 3:
            score += 15
        else:
            score += 5
        
        return float(score)
