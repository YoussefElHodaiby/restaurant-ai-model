# Quick Start Guide

Get the Restaurant AI Assistant running in 5 minutes!

## ⚡ TL;DR (Total Time: ~5 minutes)

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- DeepSeek API key (free: https://www.deepseek.com/)

### 1️⃣ Clone & Install

```bash
# Navigate to project
cd restaurant\ ai\ model

# Create .env file with your API key
echo "DEEPSEEK_API_KEY=sk_live_your_key_here" > .env

# Install dependencies
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

### 2️⃣ Start Backend (Terminal 1)

```bash
cd backend
python main.py
```

You'll see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 3️⃣ Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

You'll see:
```
  VITE v5.0.0  ready in 234 ms

  ➜  Local:   http://localhost:5173/
```

### 4️⃣ Open Browser

Navigate to: **http://localhost:5173**

### 5️⃣ Start Chatting! 💬

Type: `"I need a table for 4 tomorrow at 7 PM"`

Done! 🎉

---

## 🔧 Setup Details

### Step 1: Get DeepSeek API Key

1. Go to https://www.deepseek.com/
2. Create account
3. Copy your API key
4. Create `.env` file:

```
DEEPSEEK_API_KEY=sk_live_your_actual_key_here
```

### Step 2: Backend Setup

```bash
# Create virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
cd backend
pip install -r requirements.txt
```

**Required packages:**
- fastapi (web framework)
- uvicorn (server)
- requests (HTTP client)
- python-dotenv (environment config)

### Step 3: Frontend Setup

```bash
cd frontend
npm install
```

**Key packages:**
- react (UI)
- vite (build tool)
- axios (HTTP client)

### Step 4: Run Backend

```bash
cd backend
python main.py
```

✅ Backend ready at: http://localhost:8000

### Step 5: Run Frontend

```bash
cd frontend
npm run dev
```

✅ Frontend ready at: http://localhost:5173

---

## 🧪 Test It Works

### Test Backend API

```bash
# In a new terminal
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello!"}'
```

Should get a response like:
```json
{"reply": "Hello! Welcome to AI Restaurant..."}
```

### Test Frontend

Just open http://localhost:5173 and start typing!

---

## 🚀 Using the Chatbot

### Example Requests

**Make a reservation:**
```
"I need a table for 4 people tomorrow at 7 PM"
```

**Ask about hours:**
```
"What time are you open?"
```

**Check capacity:**
```
"How many people can you accommodate?"
```

**Request impossible time:**
```
"Can I book at 11 PM?"
```

---

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.8+

# Check if port 8000 is available
lsof -i :8000

# Install again
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend won't start

```bash
# Check Node version
node --version  # Should be 16+

# Clean and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### "API not responding" error

```bash
# Make sure backend is running
# In browser console, check:
# 1. Is http://localhost:8000 accessible?
# 2. Is backend process running?
# 3. Do you see "Uvicorn running" message?

# Restart backend
cd backend
python main.py
```

### "DEEPSEEK_API_KEY not configured"

```bash
# Create .env file in root directory
echo "DEEPSEEK_API_KEY=your_key_here" > .env

# Or manually create .env with:
# DEEPSEEK_API_KEY=sk_live_xxx
```

### Port already in use

```bash
# Change backend port
# Edit backend/main.py, last line:
# uvicorn.run(app, host="0.0.0.0", port=8001)

# Change frontend port
# Edit frontend/vite.config.js:
# port: 5174
```

---

## 📁 Project Structure

```
restaurant-ai-model/
├── backend/          # Python FastAPI app
│   └── main.py      # Start backend here
├── frontend/         # React Vite app
│   └── src/         # React components
├── tests/           # Test files
├── .env             # Your API key (CREATE THIS)
└── README.md        # Full documentation
```

---

## 🔗 Useful Links

- [Full README](README.md)
- [API Documentation](API_DOCUMENTATION.md)
- [Testing with DeepEval](DEEPEVAL_GUIDE.md)
- [Architecture](ARCHITECTURE.md)
- [Contributing](CONTRIBUTING.md)

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] DeepSeek API key obtained
- [ ] `.env` file created
- [ ] Backend dependencies installed
- [ ] Frontend dependencies installed
- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Can see chat interface at http://localhost:5173
- [ ] Chat works (got a response from AI)

---

## 🎓 Next Steps

1. **Try Different Requests**
   - Make various reservation requests
   - Test edge cases
   - See how AI responds

2. **Read the Docs**
   - Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
   - Understand [ARCHITECTURE.md](ARCHITECTURE.md)
   - Learn about [Testing](DEEPEVAL_GUIDE.md)

3. **Run Tests**
   ```bash
   pip install pytest requests
   pytest tests/test_restaurant_assistant.py -v
   ```

4. **Modify Code**
   - Change restaurant info
   - Customize UI colors
   - Add new features

5. **Learn DeepEval**
   - Read [DEEPEVAL_GUIDE.md](DEEPEVAL_GUIDE.md)
   - Write test cases
   - Evaluate AI responses

---

## 💬 Questions?

- Check README.md
- Check API_DOCUMENTATION.md
- Look at example conversations in README
- Review test cases in tests/

---

## 🎉 Success!

You now have a working AI Restaurant Assistant!

Next: Read [README.md](README.md) for complete documentation.

---

**Quick Start v1.0.0** | Last Updated: 2024-01-15
