"""
FastAPI Backend Server for AI-Assisted SEO Web Application
Serves as the API endpoint for SEO analysis and optimization
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from pathlib import Path
import os

from seo_engine import SEOEngine

# Initialize FastAPI app
app = FastAPI(
    title="SEO Analyzer API",
    description="AI-Assisted SEO Web Application for Saveetha Institute",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sample dataset
def load_dataset():
    dataset_path = Path(__file__).parent / "dataset.json"
    try:
        with open(dataset_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"courses": [], "faculty": [], "research": []}

# Initialize SEO Engine with sample corpus
DATASET = load_dataset()
CORPUS = [
    item.get("description", "") 
    for item in (DATASET.get("courses", []) + DATASET.get("faculty", []) + DATASET.get("research", []))
]

if CORPUS:
    seo_engine = SEOEngine(CORPUS)
else:
    seo_engine = None

# --- Request/Response Models ---
class SEOAnalysisRequest(BaseModel):
    url: str
    page_title: str
    meta_description: str
    page_content: str
    keywords: List[str] = []

class MetricsRequest(BaseModel):
    ground_truth: List[int]
    predictions: List[int]

class KeywordExtractionRequest(BaseModel):
    text: str
    top_n: int = 10

class OptimizationResponse(BaseModel):
    optimized_title: str
    meta_description: str
    recommended_keywords: List[str]
    keyword_scores: Dict[str, float]
    page_quality_score: float
    seo_recommendations: List[str]

# --- Health Check ---
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "SEO Analyzer API",
        "version": "1.0.0"
    }

# --- SEO Analysis Endpoints ---
@app.post("/api/analyze")
async def analyze_page(request: SEOAnalysisRequest):
    """
    Analyze a webpage for SEO optimization.
    Evaluates title, meta description, content relevance, and keyword density.
    """
    if not seo_engine:
        raise HTTPException(status_code=500, detail="SEO Engine not initialized")
    
    try:
        # Evaluate relevance of content to keywords
        relevance_score = 0.0
        if request.keywords:
            for keyword in request.keywords:
                score = seo_engine.evaluate_relevance(keyword, request.page_content)
                relevance_score += score
            relevance_score /= len(request.keywords)
        
        # Calculate page quality score
        keyword_density = (sum(request.page_content.lower().count(kw.lower()) 
                             for kw in request.keywords) / len(request.page_content.split())) * 100 if request.keywords else 0
        
        page_quality = seo_engine.calculate_page_quality_score(
            title_length=len(request.page_title),
            description_length=len(request.meta_description),
            keyword_density=keyword_density,
            anchor_text_count=request.page_content.count("<a")
        )
        
        # Get recommendations
        recommendations = seo_engine.recommend_meta_tags(request.page_title, request.page_content)
        
        seo_recommendations = [
            f"Title length is {len(request.page_title)} characters. Optimal: 30-60.",
            f"Meta description length is {len(request.meta_description)} characters. Optimal: 120-160.",
            f"Keyword density: {keyword_density:.2f}%. Optimal: 1-3%.",
            "Include internal links to improve SEO ranking."
        ]
        
        return {
            "url": request.url,
            "analysis": {
                "relevance_score": float(relevance_score),
                "page_quality_score": float(page_quality),
                "keyword_density": float(keyword_density),
                "title_analysis": {
                    "current": request.page_title,
                    "optimized": recommendations["optimized_title"],
                    "length": len(request.page_title)
                },
                "meta_analysis": {
                    "current": request.meta_description,
                    "recommended": recommendations["meta_description"],
                    "length": len(request.meta_description)
                },
                "keywords": recommendations["recommended_keywords"],
                "keyword_scores": recommendations["keyword_scores"],
                "recommendations": seo_recommendations
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@app.post("/api/metrics")
async def calculate_metrics(request: MetricsRequest):
    """
    Calculate evaluation metrics: Precision, Recall, F1-Score
    Used for measuring SEO optimization effectiveness.
    """
    if not seo_engine:
        raise HTTPException(status_code=500, detail="SEO Engine not initialized")
    
    if len(request.ground_truth) != len(request.predictions):
        raise HTTPException(status_code=400, detail="Ground truth and predictions must have equal length")
    
    try:
        metrics = seo_engine.calculate_metrics(request.ground_truth, request.predictions)
        return {
            "metrics": metrics,
            "interpretation": {
                "precision": f"Of predicted relevant pages, {metrics['precision']*100:.1f}% were actually relevant",
                "recall": f"Of all relevant pages, {metrics['recall']*100:.1f}% were correctly identified",
                "f1_score": f"Overall effectiveness score: {metrics['f1_score']:.3f}"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Metrics calculation error: {str(e)}")

@app.post("/api/keywords")
async def extract_keywords(request: KeywordExtractionRequest):
    """
    Extract top TF-IDF keywords from text content.
    Useful for meta-tag optimization and SEO recommendations.
    """
    if not seo_engine:
        raise HTTPException(status_code=500, detail="SEO Engine not initialized")
    
    try:
        keywords = seo_engine.extract_keywords(request.text, request.top_n)
        return {
            "keywords": [{"term": kw[0], "score": kw[1]} for kw in keywords],
            "total_extracted": len(keywords)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Keyword extraction error: {str(e)}")

@app.get("/api/dataset")
async def get_dataset():
    """Retrieve the academic dataset (Courses, Faculty, Research)"""
    return DATASET

@app.get("/api/dataset/courses")
async def get_courses():
    """Retrieve all courses"""
    return {"courses": DATASET.get("courses", [])}

@app.get("/api/dataset/faculty")
async def get_faculty():
    """Retrieve all faculty members"""
    return {"faculty": DATASET.get("faculty", [])}

@app.get("/api/dataset/research")
async def get_research():
    """Retrieve all research papers"""
    return {"research": DATASET.get("research", [])}

@app.post("/api/sitemaps/validate")
async def validate_sitemap(urls: List[str]):
    """
    Validate XML sitemap URLs for SEO compliance.
    """
    try:
        analysis = seo_engine.analyze_sitemaps(urls)
        return {
            "validation_status": "completed",
            "total_urls": len(urls),
            "analysis": analysis["analysis"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sitemap validation error: {str(e)}")

@app.post("/api/before-after")
async def before_after_comparison(before: SEOAnalysisRequest, after: SEOAnalysisRequest):
    """
    Compare SEO metrics before and after optimization.
    Returns improvement percentages for Precision, Recall, F1-Score.
    """
    if not seo_engine:
        raise HTTPException(status_code=500, detail="SEO Engine not initialized")
    
    try:
        before_analysis = await analyze_page(before)
        after_analysis = await analyze_page(after)
        
        before_score = before_analysis["analysis"]["page_quality_score"]
        after_score = after_analysis["analysis"]["page_quality_score"]
        improvement = ((after_score - before_score) / before_score * 100) if before_score > 0 else 0
        
        return {
            "before": before_analysis["analysis"],
            "after": after_analysis["analysis"],
            "improvement_percentage": float(improvement),
            "metrics_comparison": {
                "quality_score_before": float(before_score),
                "quality_score_after": float(after_score),
                "relevance_improvement": float(after_analysis["analysis"]["relevance_score"] - before_analysis["analysis"]["relevance_score"])
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
