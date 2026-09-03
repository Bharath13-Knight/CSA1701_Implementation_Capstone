# AI-Assisted SEO Web Application for Saveetha Institute

## Project Overview

SEO Analyzer Pro is a full-stack web application designed to help optimize website search engine performance. It combines:

- **Backend**: FastAPI with Python NLP/ML algorithms (TF-IDF, Cosine Similarity, Precision/Recall/F1-Score metrics)
- **Frontend**: React with Vite for interactive dashboards and analytics visualization
- **Dataset**: Academic dataset from Saveetha Institute (Courses, Faculty, Research)

---

## Project Structure

```
AI Assignment/
├── backend/
│   ├── main.py              # FastAPI server with SEO analysis endpoints
│   ├── seo_engine.py        # Core SEO Engine (TF-IDF, metrics, keyword extraction)
│   ├── dataset.json         # Sample academic dataset
│   └── requirements.txt     # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx          # Main React component
│   │   ├── App.css          # Styling
│   │   └── main.jsx         # React entry point
│   ├── index.html           # HTML template
│   ├── package.json         # npm dependencies
│   ├── vite.config.js       # Vite configuration
│   └── .env                 # Environment variables
│
├── Artificial Intelligence.py (empty - ready for custom implementation)
├── green_backend_api.py     (existing file)
└── README.md                # This file
```

---

## Requirements Checklist

### Software & Runtimes
- ✅ **Python 3.10+** - For backend AI/ML algorithms
- ✅ **Node.js 18+** - For React frontend
- ✅ **VS Code** - Recommended IDE

### VS Code Extensions (Optional but Recommended)
- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Thunder Client** or **Postman** (for API testing)
- **ES7+ React/Redux snippets** (dsznajder.es7-react-js-snippets)

---

## Quick Start

### Step 1: Install Backend Dependencies

Open a terminal in the `backend/` directory and run:

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm  # Optional NLP model
```

**Dependencies installed:**
- `fastapi==0.104.1` - Web framework
- `uvicorn==0.24.0` - ASGI server
- `scikit-learn==1.3.2` - ML metrics & TF-IDF
- `numpy==1.26.2` - Numerical computing
- `pandas==2.1.1` - Data processing
- `beautifulsoup4==4.12.2` - HTML/XML parsing
- `pydantic==2.5.0` - Data validation

### Step 2: Start Backend Server

In the `backend/` directory:

```bash
python -m uvicorn main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

Visit the API documentation: http://localhost:8000/docs

### Step 3: Install Frontend Dependencies

Open a terminal in the `frontend/` directory and run:

```bash
npm install
```

**Key packages:**
- `react@18.2.0` - UI framework
- `vite@5.0.8` - Build tool & dev server
- `axios` - HTTP client
- `recharts` - Data visualization
- `lucide-react` - Icon library

### Step 4: Start Frontend Development Server

In the `frontend/` directory:

```bash
npm run dev
```

Expected output:
```
  VITE v5.0.8  ready in 234 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

Open http://localhost:5173 in your browser.

---

## API Endpoints

### Health Check
- **GET** `/health`

### SEO Analysis
- **POST** `/api/analyze` - Analyze a webpage for SEO optimization
- **POST** `/api/before-after` - Compare before/after optimization metrics

### Keyword Analysis
- **POST** `/api/keywords` - Extract top TF-IDF keywords from text

### Evaluation Metrics
- **POST** `/api/metrics` - Calculate Precision, Recall, F1-Score

### Sitemaps
- **POST** `/api/sitemaps/validate` - Validate XML sitemap URLs

### Dataset
- **GET** `/api/dataset` - Get full academic dataset
- **GET** `/api/dataset/courses` - Get courses only
- **GET** `/api/dataset/faculty` - Get faculty only
- **GET** `/api/dataset/research` - Get research papers only

---

## Testing the Application

### 1. Using the Frontend UI
1. Navigate to http://localhost:5173
2. Go to the **"Analyze Page"** tab
3. Fill in sample data:
   - URL: `https://example.com`
   - Title: `Best Computer Science Course at Saveetha`
   - Description: `Learn computer science fundamentals`
   - Content: `Paste course description here...`
   - Keywords: `computer science, programming, algorithms`
4. Click **"Analyze Page"**

### 2. Using API Documentation (Swagger)
1. Navigate to http://localhost:8000/docs
2. Try out endpoints directly in the interactive Swagger UI

### 3. Using cURL
```bash
curl -X POST "http://localhost:8000/api/keywords" \
  -H "Content-Type: application/json" \
  -d '{"text": "Artificial intelligence and machine learning", "top_n": 5}'
```

### 4. Using Thunder Client (VS Code Extension)
1. Install Thunder Client extension
2. Create a new request
3. Select POST method
4. Enter URL: `http://localhost:8000/api/analyze`
5. Add JSON body with analysis data
6. Send

---

## Features Implemented

### Backend Features
✅ **TF-IDF Vectorization** - Extract important keywords from content
✅ **Cosine Similarity** - Measure relevance between query and page content
✅ **Precision/Recall/F1-Score** - Evaluate SEO optimization effectiveness (CO5/BL6)
✅ **Page Quality Scoring** - 0-100 score based on:
   - Title optimization (30-60 characters)
   - Meta description (120-160 characters)
   - Keyword density (1-3%)
   - Internal link count
✅ **Meta-tag Optimization** - Generate improved titles and descriptions
✅ **Keyword Extraction** - Extract top N keywords with TF-IDF scores
✅ **Sitemap Validation** - Validate URLs for SEO compliance
✅ **Before/After Comparison** - Track improvement metrics

### Frontend Features
✅ **Page Analyzer** - Analyze single webpage for SEO issues
✅ **Keyword Extractor** - Interactive TF-IDF keyword extraction
✅ **Metrics Dashboard** - Visualize Precision/Recall/F1-Score
✅ **Dataset Browser** - Explore Saveetha Institute courses, faculty, research
✅ **Responsive Design** - Mobile-friendly UI
✅ **Real-time Charts** - Visualize metrics with Recharts

---

## Rubric Alignment (CO5 & BL6)

### CO5: Apply appropriate AI algorithms
✅ **TF-IDF Vectorization** - Implemented in `SEOEngine.extract_keywords()`
✅ **Cosine Similarity** - Implemented in `SEOEngine.evaluate_relevance()`
✅ **Machine Learning Metrics** - Precision, Recall, F1-Score in `SEOEngine.calculate_metrics()`

### BL6: Evaluate effectiveness of solution
✅ **Before/After Comparison** - `/api/before-after` endpoint
✅ **Page Quality Score** - `calculate_page_quality_score()` method
✅ **Metric Visualization** - Charts and graphs on frontend

---

## Build & Deployment

### Build Frontend
```bash
cd frontend
npm run build
```

Output in `frontend/dist/` folder.

### Production Start Backend
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sklearn'"
**Solution:** Run `pip install scikit-learn`

### Issue: Backend not accessible from frontend
**Solution:** Ensure CORS is enabled in `backend/main.py` (it is by default)

### Issue: Port 8000 already in use
**Solution:** 
```bash
uvicorn main:app --port 8001 --reload
```
Then update frontend `.env` to point to port 8001

### Issue: React won't start
**Solution:** 
```bash
npm cache clean --force
npm install
npm run dev
```

---

## Next Steps for Enhancement

1. **Database Integration** - Replace JSON with PostgreSQL/Firebase
2. **Authentication** - Add user login/registration
3. **Batch Processing** - Analyze multiple URLs simultaneously
4. **Real XML Sitemap Parsing** - Parse actual sitemap.xml files
5. **Advanced NLP** - Add spaCy entity extraction
6. **Report Generation** - Export PDF/Excel reports
7. **Caching** - Implement Redis for performance
8. **Testing** - Add pytest + Jest test suites

---

## Contact & Support

For questions or issues, refer to the API documentation at:
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

**Last Updated:** September 2024
**Version:** 1.0.0
