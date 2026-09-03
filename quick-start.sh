#!/bin/bash
# Quick Start Script for SEO Analyzer Pro
# Linux/Mac

echo "============================================"
echo "SEO Analyzer Pro - Quick Start"
echo "============================================"
echo ""

echo "[1/4] Checking Python..."
python3 --version || {
    echo "ERROR: Python not found. Please install Python 3.10+"
    exit 1
}

echo ""
echo "[2/4] Installing Backend Dependencies..."
cd backend || exit 1
pip install -r requirements.txt || {
    echo "ERROR: Failed to install backend dependencies"
    exit 1
}

cd ..

echo ""
echo "[3/4] Checking Node.js..."
node --version || {
    echo "ERROR: Node.js not found. Please install Node.js 18+"
    exit 1
}

echo ""
echo "[4/4] Installing Frontend Dependencies..."
cd frontend || exit 1
npm install || {
    echo "ERROR: Failed to install frontend dependencies"
    exit 1
}

cd ..

echo ""
echo "============================================"
echo "Installation Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Start Backend:"
echo "   cd backend"
echo "   python -m uvicorn main:app --reload"
echo "   (Visit: http://localhost:8000/docs)"
echo ""
echo "2. Start Frontend (in a new terminal):"
echo "   cd frontend"
echo "   npm run dev"
echo "   (Visit: http://localhost:5173)"
echo ""
echo "============================================"
