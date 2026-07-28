# Architecture Overview

This document explains the architecture and design decisions of the Restaurant AI Assistant application.

## 🏗️ High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser                               │
│  (Chrome, Firefox, Safari, Edge)                             │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (React + Vite)                   │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ • Chatbot UI Component                                  │ │
│  │ • Message History Display                               │ │
│  │ • Input Field & Send Button                             │ │
│  │ • Responsive CSS Design                                 │ │
│  │ • Axios HTTP Client                                     │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Port: 5173 (Development) / Served by Nginx (Production)   │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/JSON
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  Backend (FastAPI + Python)                  │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ FastAPI Server (Uvicorn)                                │ │
│  │                                                          │ │
│  │ • POST /chat - Chat endpoint                            │ │
│  │ • GET /reservations - Get reservations                  │ │
│  │ • GET / - Health check                                  │ │
│  │ • CORS Middleware                                       │ │
│  │                                                          │ │
│  │ Restaurant Logic:                                       │ │
│  │ • Business rules enforcement                            │ │
│  │ • Table availability checking                           │ │
│  │ • Reservation storage (in-memory)                       │ │
│  │                                                          │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                              │
│  Port: 8000                                                 │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTPS/API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│               External LLM Service (DeepSeek)                │
│                                                              │
│  • Chat Completions API                                     │
│  • Model: deepseek-chat                                     │
│  • API Key: Stored in .env                                  │
│  • Endpoint: https://api.deepseek.com/chat/completions     │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
restaurant-ai-model/
├── frontend/                      # React Vite application
│   ├── src/
│   │   ├── App.jsx               # Main chat component
│   │   ├── App.css               # Styling
│   │   └── main.jsx              # Entry point
│   ├── index.html                # HTML template
│   ├── vite.config.js            # Vite configuration
│   ├── package.json              # Dependencies
│   ├── Dockerfile                # Container configuration
│   └── .dockerignore             # Docker ignore patterns
│
├── backend/                       # Python FastAPI application
│   ├── main.py                   # FastAPI app & endpoints
│   ├── requirements.txt          # Python dependencies
│   ├── Dockerfile                # Container configuration
│   └── .dockerignore             # Docker ignore patterns
│
├── tests/                        # Test suite
│   ├── test_restaurant_assistant.py  # Integration tests
│   └── conftest.py               # Pytest configuration
│
├── .github/
│   └── workflows/
│       └── ci.yml               # CI/CD pipeline
│
├── docker-compose.yml            # Multi-container orchestration
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore patterns
├── Makefile                      # Development commands
├── requirements-dev.txt          # Dev dependencies
├── README.md                     # Main documentation
├── API_DOCUMENTATION.md          # API reference
├── DEEPEVAL_GUIDE.md            # LLM testing guide
├── CONTRIBUTING.md              # Contribution guidelines
└── ARCHITECTURE.md              # This file
```

## 🔄 Data Flow

### 1. User Sends Message

```
User Types Message
       ↓
User Clicks "Send" Button
       ↓
React Component Captures Input
       ↓
Frontend Prepares JSON Payload
       ↓
Axios Sends POST Request to /chat
```

### 2. Backend Processes Message

```
FastAPI Receives Request
       ↓
Validates Input (Pydantic)
       ↓
Loads Restaurant Information
       ↓
Gets Current Reservations from Memory
       ↓
Generates System Prompt with Context
       ↓
Calls DeepSeek API
       ↓
Processes Response
       ↓
Returns JSON Response
```

### 3. Frontend Displays Response

```
Axios Receives Response
       ↓
React State Updates
       ↓
Component Re-renders
       ↓
Message Appears in Chat
       ↓
User Sees Assistant's Reply
```

## 🎯 Technology Choices

### Frontend: React + Vite

**Why React?**
- Component-based architecture is beginner-friendly
- Large ecosystem and community
- Virtual DOM for efficient updates
- Good for learning modern JavaScript

**Why Vite?**
- Extremely fast development server
- Simple configuration (minimal boilerplate)
- Fast builds with esbuild
- Perfect for learning projects

**Why Axios?**
- Simple HTTP client
- Good error handling
- Easy to understand for beginners

### Backend: FastAPI + Python

**Why FastAPI?**
- Modern Python web framework
- Automatic API documentation (Swagger)
- Built-in data validation with Pydantic
- Easy to learn and understand
- Great for teaching

**Why Python?**
- Readable and beginner-friendly syntax
- Excellent for LLM integration
- Rich ecosystem for AI/ML
- Industry standard for data science

**Why Uvicorn?**
- Fast ASGI server
- Lightweight and easy to use
- Perfect for development and production

### LLM Integration: DeepSeek API

**Why DeepSeek?**
- Cost-effective
- Good quality responses
- Simple API
- No complex setup needed

**Why Not Local LLM?**
- For teaching simplicity
- No GPU required
- Consistent results
- Easier to test

## 🔐 Security Considerations

### Current (Demo)
- No authentication required
- API key in environment variable only
- CORS enabled for localhost

### Production Recommendations
```python
# Implement authentication
from fastapi.security import HTTPBearer

# Add rate limiting
from slowapi import Limiter

# Use HTTPS/TLS
# Add input validation
# Sanitize outputs
# Implement logging
# Add request signing
```

## 💾 Data Storage

### Current Architecture
```python
# In-memory storage
reservations = [
    {
        "name": "John Doe",
        "party_size": 4,
        "time": "7:00 PM",
        "table_id": 3,
        "date": "2024-01-15"
    }
]
```

### Limitations
- Data lost on server restart
- Not suitable for production
- No concurrent access protection

### Production Upgrade Path
```
In-Memory → SQLite → PostgreSQL → MongoDB
```

## 🧠 AI Assistant Design

### System Prompt Architecture

```python
def get_system_prompt():
    return f"""
    You are a restaurant reservation assistant.
    
    Restaurant: {RESTAURANT_INFO}
    Current Reservations: {reservations}
    Rules: {RESERVATION_RULES}
    """
```

**Why This Approach?**
- Context is rebuilt for each request
- Easy to modify rules
- Simple for testing
- Beginner-friendly

### Alternative Approaches (Not Used)

1. **Fine-tuning**: Too expensive and complex
2. **RAG (Retrieval)**: Overkill for this use case
3. **Tools/Functions**: Good, but complex for beginners
4. **Memory Management**: Not needed for demo

## 📊 Performance Architecture

### Response Times
```
Frontend Input → Browser: <1ms
Browser → Backend: 50-200ms (network)
Backend → DeepSeek: 1000-3000ms (LLM processing)
DeepSeek → Backend: 1000-3000ms (network + processing)
Backend → Frontend: 50-200ms (network)
Frontend Render: <100ms
Total: ~2-7 seconds
```

### Optimization Strategies
1. **Frontend**
   - Lazy loading
   - Component memoization
   - CSS-in-JS minimization

2. **Backend**
   - Connection pooling
   - Caching responses
   - Async processing

3. **LLM**
   - Shorter prompts
   - Lower token limits
   - Response caching

## 🧪 Testing Architecture

### Test Layers
```
┌─────────────────────────────────────────┐
│  E2E Tests (Playwright)                 │ ← Frontend UI
├─────────────────────────────────────────┤
│  Integration Tests (Pytest)             │ ← API endpoints
├─────────────────────────────────────────┤
│  LLM Quality Tests (DeepEval)           │ ← Response quality
├─────────────────────────────────────────┤
│  Unit Tests (Pytest, Jest)              │ ← Individual functions
└─────────────────────────────────────────┘
```

### Testing Strategy
1. **Unit Tests**: Test helper functions
2. **Integration Tests**: Test API endpoints
3. **LLM Tests**: Test AI response quality
4. **E2E Tests**: Test full user flow

## 🐳 Containerization

### Docker Architecture
```
┌─────────────────────────────────────────┐
│        Docker Compose Network            │
├─────────────────────────────────────────┤
│                                         │
│  ┌───────────────────┐   ┌────────────┐ │
│  │ Backend Container │   │ Frontend   │ │
│  │ • Python 3.11     │   │ Container  │ │
│  │ • FastAPI         │   │ • Node 18  │ │
│  │ • Uvicorn         │   │ • Vite     │ │
│  │ Port: 8000        │   │ • Serve    │ │
│  └───────────────────┘   │ Port: 5173 │ │
│           ▲               └────────────┘ │
│           │                              │
│           └──── restaurant_network       │
│                                         │
└─────────────────────────────────────────┘
```

### Build Optimization
- Multi-stage builds for frontend
- Alpine base images
- Minimal dependencies
- .dockerignore files

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow

```yaml
┌──────────┐
│  Push    │
└────┬─────┘
     ▼
┌──────────────────────┐
│  Run Tests           │ ← pytest, jest
│  Lint Code           │ ← flake8, eslint
│  Security Scan       │ ← safety, npm audit
│  Build Docker Images │ ← backend, frontend
└────┬─────────────────┘
     ▼
┌──────────┐
│  Status  │ ✅ Pass / ❌ Fail
└──────────┘
```

## 🌐 Deployment Architecture (Future)

### Recommended Setup
```
┌─────────────────────────────────────────────┐
│             Internet / Users                │
└────────────────────┬────────────────────────┘
                     ▼
        ┌────────────────────────┐
        │  Nginx / Load Balancer │
        └────────┬───────────────┘
                 ▼
        ┌────────────────────┐
        │  Frontend Container│
        │  (React SPA)       │
        └────────────────────┘
                 ▼
        ┌────────────────────┐
        │  Backend Container │
        │  (FastAPI)         │
        └────────┬───────────┘
                 ▼
      ┌──────────────────────┐
      │  Database (Optional) │
      │  • PostgreSQL        │
      │  • MongoDB           │
      └──────────────────────┘
```

## 📈 Scalability Considerations

### Current Limitations
- Single backend instance
- In-memory storage
- No load balancing
- No caching layer

### Scaling Strategies

1. **Horizontal Scaling**
   - Docker Compose → Kubernetes
   - Load balancer (Nginx)
   - Multiple backend replicas

2. **Vertical Scaling**
   - Larger server
   - More CPU/RAM
   - Faster connection

3. **Data Persistence**
   - Move from in-memory to database
   - Add Redis for caching
   - Implement connection pooling

## 🎓 Learning Outcomes

By studying this architecture, you'll learn:

1. **Frontend**
   - React component lifecycle
   - State management
   - HTTP requests with Axios
   - CSS styling

2. **Backend**
   - FastAPI framework
   - RESTful API design
   - Request/response handling
   - Error handling

3. **LLM Integration**
   - API integration
   - Prompt engineering
   - Response processing

4. **DevOps**
   - Docker containerization
   - CI/CD pipelines
   - Environment configuration

5. **Testing**
   - Unit testing
   - Integration testing
   - LLM quality testing

## 🔧 Extending the Architecture

### Adding Features

1. **Database**
   ```python
   # Replace in-memory with SQLAlchemy
   from sqlalchemy import create_engine
   database = create_engine("sqlite:///reservations.db")
   ```

2. **Authentication**
   ```python
   # Add JWT tokens
   from fastapi.security import HTTPBearer
   security = HTTPBearer()
   ```

3. **Caching**
   ```python
   # Add Redis
   from redis import Redis
   cache = Redis(host='localhost', port=6379)
   ```

4. **Real-time Updates**
   ```python
   # Add WebSockets
   from fastapi import WebSocket
   @app.websocket("/ws")
   async def websocket_endpoint(websocket: WebSocket):
   ```

## 📚 Architecture Patterns Used

1. **MVC (Model-View-Controller)**
   - Frontend: View
   - Backend: Model + Controller
   - Database: Model (future)

2. **REST API Pattern**
   - Resource-based endpoints
   - Standard HTTP methods
   - JSON communication

3. **Component-Based Architecture**
   - React components
   - Reusable pieces
   - Composition over inheritance

4. **Middleware Pattern**
   - CORS middleware
   - Error handling
   - Logging (future)

## 🚀 Future Improvements

- [ ] Add database persistence
- [ ] Implement user authentication
- [ ] Add real-time notifications (WebSockets)
- [ ] Implement caching (Redis)
- [ ] Add comprehensive logging
- [ ] Performance monitoring
- [ ] Advanced error handling
- [ ] API versioning

---

**Architecture Document v1.0.0** | Last Updated: 2024-01-15

For more information, see:
- [README.md](README.md)
- [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- [DEEPEVAL_GUIDE.md](DEEPEVAL_GUIDE.md)
