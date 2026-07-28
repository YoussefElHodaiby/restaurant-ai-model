# Restaurant AI Reservation Assistant

A full-stack web application demonstrating how to build and test AI-powered chatbots using **DeepEval** for LLM testing.

This project serves as a practical example for teaching clean code, modern web development, and LLM testing best practices.

## 🎯 Purpose

This is a **teaching project** for demonstrating:
- Full-stack AI application architecture
- LLM integration with FastAPI and React
- Testing LLM outputs with DeepEval
- Clean, beginner-friendly code practices

## 🏗️ Tech Stack

### Frontend
- **React 18** - UI framework
- **Vite** - Fast build tool and dev server
- **Axios** - HTTP client
- **CSS3** - Modern styling

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - Modern web framework
- **Uvicorn** - ASGI server
- **Requests** - HTTP library
- **python-dotenv** - Environment configuration

### LLM
- **DeepSeek API** - AI model provider
- API key stored in `.env` file

## 📋 Features

### Chatbot Interface
- **Responsive Design** - Works on desktop and mobile
- **Conversation History** - View entire chat history
- **Real-time Responses** - Live streaming of AI replies
- **Clean UI** - Beginner-friendly interface

### Restaurant Reservation Logic
- **AI-Powered Assistant** - Uses DeepSeek to understand requests
- **Restaurant Information**:
  - Name: AI Restaurant
  - Hours: 11 AM - 10 PM
  - Tables: 5 tables with capacities 2, 2, 4, 4, 6

### Business Rules
- ✅ Only accept reservations within business hours (11 AM - 10 PM)
- ✅ Maximum reservation duration: 2 hours
- ✅ Suggest alternatives if tables are unavailable
- ✅ Match party size with appropriate tables
- ✅ Always respond politely and professionally

### Storage
- **No Database** - Reservations stored in memory only (demo purposes)
- **No Authentication** - Open access for teaching
- **Simplified Backend** - Easy to understand and extend

## 📁 Project Structure

```
restaurant-ai-model/
├── backend/
│   ├── main.py                 # FastAPI application
│   └── requirements.txt         # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Main chat component
│   │   └── App.css             # Styling
│   ├── index.html              # HTML template
│   ├── vite.config.js          # Vite configuration
│   └── package.json            # NPM dependencies
├── .env.example                # Environment template
└── README.md                   # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- DeepSeek API key (get from https://www.deepseek.com/)

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp ../.env.example ../.env

# Edit .env and add your DeepSeek API key
# DEEPSEEK_API_KEY=sk_live_xxxxxxxxxxxxxxxx
```

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

### 3. Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
source venv/bin/activate  # Or venv\Scripts\activate on Windows
python main.py
```

Backend will run at: `http://localhost:8000`

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will run at: `http://localhost:5173`

### 4. Open in Browser

Navigate to: `http://localhost:5173`

## 💬 API Endpoint

### POST /chat

Send a message to the restaurant AI assistant.

**Request:**
```json
{
  "message": "I need a table for 4 tomorrow at 7 PM"
}
```

**Response:**
```json
{
  "reply": "I'd be happy to help! Let me check our availability for 4 people tomorrow at 7 PM. We have Table 3 (capacity 4) available. Would you like me to confirm this reservation for you?"
}
```

### GET /reservations

Get all current reservations (for debugging).

**Response:**
```json
{
  "reservations": [
    {
      "name": "Customer",
      "party_size": 4,
      "time": "7:00 PM",
      "table_id": 3,
      "date": "2024-01-15"
    }
  ]
}
```

### GET /

Health check endpoint.

**Response:**
```json
{
  "status": "Restaurant AI Assistant API running"
}
```

## 🧪 Testing with DeepEval

This project is designed to be tested with DeepEval. Example test scenarios:

```python
# Test: Assistant understands reservation requests
# Test: Assistant respects business hours
# Test: Assistant suggests alternatives when unavailable
# Test: Responses are polite and professional
```

See DeepEval documentation for implementing these tests.

## 📝 Example Conversations

### Example 1: Valid Reservation
```
User: "I need a table for 2 people tomorrow at 8 PM"
Bot: "I'd be happy to help! For 2 people, I can offer you Table 1 or Table 2. Both have a capacity of 2. Would 8 PM tomorrow work for you? Your reservation would end at 10 PM."
```

### Example 2: Outside Business Hours
```
User: "Can we reserve a table for 4 at 11 PM?"
Bot: "I'm sorry, but our restaurant closes at 10 PM. We're open from 11 AM to 10 PM. Would you like to book a table earlier in the evening?"
```

### Example 3: Party Too Large
```
User: "I need a table for 8 people at 6 PM"
Bot: "I'm sorry, but our largest table seats 6 people. Would you be able to split into two groups, or would 6 people work for your party?"
```

## 🛠️ Customization

### Change Restaurant Information

Edit `backend/main.py`, `RESTAURANT_INFO` dictionary:

```python
RESTAURANT_INFO = {
    "name": "Your Restaurant Name",
    "hours": "10 AM - 11 PM",
    "tables": [
        {"id": 1, "capacity": 2},
        {"id": 2, "capacity": 4},
        # Add more tables...
    ],
    "max_duration_hours": 3,
}
```

### Modify Frontend Colors

Edit `frontend/src/App.css` gradient colors:

```css
background: linear-gradient(135deg, #YOUR_COLOR_1 0%, #YOUR_COLOR_2 100%);
```

### Adjust AI Response Temperature

Edit `backend/main.py`, `/chat` endpoint:

```python
"temperature": 0.5,  # Lower = more deterministic, Higher = more creative
```

## ⚙️ Environment Variables

Create `.env` file in the root directory:

```env
# Required
DEEPSEEK_API_KEY=sk_live_your_key_here

# Optional
VITE_API_URL=http://localhost:8000
```

## 🐛 Troubleshooting

### Backend Issues

**Error: "DEEPSEEK_API_KEY not configured"**
- Create `.env` file in root directory
- Add your DeepSeek API key
- Restart the backend

**Error: "Connection refused"**
- Make sure backend is running: `python main.py`
- Check it's on port 8000: `http://localhost:8000`

### Frontend Issues

**Error: "Cannot find module 'axios'"**
- Run `npm install` in frontend directory

**Chat not working**
- Open browser DevTools (F12) and check Console
- Verify backend is running
- Check Network tab for failed requests

**Port 5173 already in use**
- Kill existing process or change port in `vite.config.js`

## 📚 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [DeepSeek API](https://www.deepseek.com/)
- [DeepEval Documentation](https://docs.confident-ai.com/)

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

This is a teaching project. Feel free to:
- Add features for learning
- Improve code examples
- Fix bugs
- Enhance documentation

## 💡 Next Steps

1. **Add DeepEval Tests** - Implement LLM output testing
2. **Add Database** - Replace in-memory storage with SQLite/PostgreSQL
3. **Add Authentication** - Implement user login
4. **Add Real Reservations** - Send confirmation emails
5. **Deploy** - Deploy to cloud (Heroku, AWS, Azure)

## 📧 Questions?

This is a teaching project. Review the code, modify it, and learn!

---

**Happy Coding! 🚀**
