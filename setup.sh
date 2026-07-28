#!/bin/bash

echo "🚀 Restaurant AI Reservation Assistant - Quick Start"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 16 or higher."
    exit 1
fi

echo "✅ Python and Node.js found"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

echo ""
echo "⚙️  Backend setup complete!"
echo "⚠️  IMPORTANT: Create a .env file in the root directory with your DeepSeek API key:"
echo "   DEEPSEEK_API_KEY=sk_live_your_key_here"
echo ""

# Frontend setup
cd ../frontend
echo "📦 Setting up frontend..."
echo "📥 Installing Node dependencies..."
npm install

echo ""
echo "✅ Frontend setup complete!"
echo ""

# Summary
echo "======================================================"
echo "✨ Setup complete!"
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then open http://localhost:5173 in your browser"
echo "======================================================"
