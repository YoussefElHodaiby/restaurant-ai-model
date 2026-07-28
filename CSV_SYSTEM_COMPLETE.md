# ✅ COMPLETE: CSV-Based AI Restaurant System

## 🎉 What You Have Built

A **production-ready AI restaurant reservation system** that uses **CSV files as the complete knowledge base**:

### Core Components

#### 1. **Backend (FastAPI + Ollama)**
- **Location:** `backend/main.py`
- **Port:** 8000
- **Features:**
  - Loads `business_info.csv` on startup
  - Loads `reservations.csv` for existing bookings
  - Generates dynamic system prompts from CSV data
  - Integrates with local Ollama model (Gemma 3 4B)
  - Validates reservations using CSV business rules
  - Persists bookings to CSV files

#### 2. **Frontend (React + Vite)**
- **Location:** `frontend/src/App.jsx`
- **Port:** 5174
- **Features:**
  - 4-section Italian restaurant website
  - Menu browsing with dishes from CSV
  - AI chatbot for reservations
  - Beautiful UI with red/gold Italian theme

#### 3. **Knowledge Base Files (CSVs)**
- **business_info.csv** - All restaurant knowledge
- **reservations.csv** - All bookings (auto-created & updated)

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     CSV KNOWLEDGE BASE                          │
├──────────────────────┬──────────────────────┬──────────────────┤
│  business_info.csv   │  reservations.csv    │  Menu            │
│  ├─ Restaurant name  │  ├─ Table ID        │  ├─ Dishes       │
│  ├─ Hours           │  ├─ Dates/Times     │  ├─ Prices       │
│  ├─ Address         │  ├─ Party size      │  └─ Descriptions │
│  ├─ Menu items      │  ├─ Dishes ordered  │                  │
│  ├─ Tables (1-10)   │  └─ Timestamps      │  Dietary         │
│  └─ Policies        │                     │  ├─ Vegetarian   │
└──────────────────────┴──────────────────────┴──────────────────┘
              ↓                    ↓
         [Backend Loads CSVs on startup]
              ↓
    ┌─────────────────────────────┐
    │  System Prompt Generation   │
    │  ├─ Restaurant details      │
    │  ├─ Full menu               │
    │  ├─ Available tables        │
    │  ├─ Current reservations    │
    │  ├─ Business rules          │
    │  └─ Dietary info            │
    └─────────────────────────────┘
              ↓
    ┌─────────────────────────────┐
    │  Ollama (Local AI Model)    │
    │  Gemma 3 4B                 │
    └─────────────────────────────┘
              ↓
    ┌─────────────────────────────┐
    │  Response Processing        │
    │  ├─ Extract reservation     │
    │  ├─ Extract dishes          │
    │  ├─ Validate rules          │
    │  └─ Save to CSV             │
    └─────────────────────────────┘
              ↓
    ┌─────────────────────────────┐
    │  reservations.csv Updated   │
    │  └─ New booking appended    │
    └─────────────────────────────┘
```

---

## 🔑 Key Features

### ✅ Document-Based Prompting
- AI reads ALL knowledge from `business_info.csv`
- System prompt is dynamically built from CSV data
- No hardcoded values in Python code
- Perfect for teaching LLM integration patterns

### ✅ Automatic Reservation Persistence
- Bookings saved to `reservations.csv` automatically
- Survives server restarts
- Human-readable CSV format
- Easy to export/analyze

### ✅ Business Logic from CSV
- Opening/closing hours from CSV
- Max party size from CSV
- Table capacities from CSV
- Menu items from CSV
- Policies from CSV

### ✅ Zero-Config Customization
- Change restaurant info by editing CSV
- Add dishes without code changes
- Modify policies without recompiling
- Restart backend to load new data

### ✅ Complete Reservation System
- 10 tables with different capacities
- Prevents double-booking (checks overlaps)
- Validates business hours
- Extracts dishes from natural language
- Tracks customer preferences

### ✅ Perfect for Teaching
- Shows real-world LLM usage
- Demonstrates RAG (Retrieval-Augmented Generation)
- Great for DeepEval testing
- Data-driven AI development
- Clear separation of data and logic

---

## 📋 CSV Files Structure

### business_info.csv (Knowledge Base)
```
key                  | value                           | category
name                 | Bella Italia                    | restaurant
open_hour            | 11                              | operations
close_hour           | 22                              | operations
dish_1               | Bruschetta|Appetizers|$8|...   | menu
table_1              | Table 1 (Cozy Corner)|2         | tables
policy_1             | Only accept 11AM-10PM           | policies
vegetarian_options   | Mozzarella|Bruschetta|...       | dietary
```

### reservations.csv (Bookings)
```
table_id | date      | time_start | party_size | dishes
4        | 2026-07-29| 19:00      | 4          | Margherita, Tiramisu
7        | 2026-07-29| 20:00      | 6          | Spaghetti al Carbonara, Tiramisu
```

---

## 🚀 How to Use

### 1. Start the Backend
```bash
cd backend
python3 main.py
```
✅ Loads business_info.csv and reservations.csv on startup

### 2. Start the Frontend
```bash
cd frontend
npm install  # First time only
npm run dev
```
✅ Opens at http://localhost:5174

### 3. Make a Booking
Go to http://localhost:5174 → Click "Reserve" → Chat with AI:
```
User: "Book 4 people tomorrow at 7 PM. I want margherita and tiramisu"
AI: "✅ [RESERVATION CONFIRMED - Table 4...]"
```

### 4. Verify CSV Persistence
```bash
# Check API
curl http://localhost:8000/reservations

# Or view file directly
cat backend/reservations.csv
```

---

## 🎨 Customization Examples

### Add New Dish
**Edit:** `backend/business_info.csv`

Add:
```
dish_14,Risotto ai Tartufi|Pasta|$32|Black truffle risotto,menu
```

**Result:** Next booking mentioning "truffle risotto" will be recognized ✅

### Change Hours
**Edit:** `backend/business_info.csv`

Change from:
```
open_hour,11,operations
close_hour,22,operations
```

To:
```
open_hour,12,operations
close_hour,23,operations
```

**Result:** System will only accept bookings 12 PM - 11 PM ✅

### Add Dietary Option
**Edit:** `backend/business_info.csv`

Add:
```
vegan_options,Bruschetta|Margherita|Panna Cotta|Gelato Trio,dietary
```

**Result:** AI can answer "What are your vegan options?" ✅

---

## 📡 API Reference

### POST /chat - Chat with AI
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book 4 people tomorrow at 7 PM"}'
```

**Response:**
```json
{
  "reply": "✅ [RESERVATION CONFIRMED - Table 4 (Family) has been reserved for 4 people on 2026-07-29 at 19:00 for 2 hours | Dishes: Margherita, Tiramisu]"
}
```

### GET /reservations - View All Bookings
```bash
curl http://localhost:8000/reservations
```

**Response:**
```json
{
  "total_reservations": 2,
  "reservations": [
    {
      "table_id": "4",
      "date": "2026-07-29",
      "time_start": "19:00",
      "time_end": "21:00",
      "party_size": "4",
      "name": "Guest",
      "dishes": "Margherita, Tiramisu",
      "created_at": "2026-07-28T20:11:38.493557"
    }
  ]
}
```

---

## 🧪 Testing the System

### Test 1: Q&A from CSV
```bash
curl -X POST http://localhost:8000/chat \
  -d '{"message": "What are your hours? Do you have vegetarian options?"}'
```
✅ AI uses CSV knowledge to answer

### Test 2: Booking with Dish Recognition
```bash
curl -X POST http://localhost:8000/chat \
  -d '{"message": "Book 2 people tomorrow at 8 PM. Spaghetti carbonara and tiramisu"}'
```
✅ Dishes from CSV menu are recognized

### Test 3: Business Rules Validation
```bash
curl -X POST http://localhost:8000/chat \
  -d '{"message": "Book 10 people tomorrow at 7 PM"}'
```
✅ Rejected (exceeds max party size from CSV)

### Test 4: CSV Persistence
```bash
curl http://localhost:8000/reservations | jq '.total_reservations'
```
✅ Bookings saved to CSV file

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `CSV_QUICK_START.md` | Quick start guide with examples |
| `CSV_KNOWLEDGE_BASE.md` | Complete CSV system documentation |
| `CSV_DEMONSTRATION.md` | Live testing scenarios & test ideas |
| `README.md` | Project overview |
| `ARCHITECTURE.md` | System design details |
| `API_DOCUMENTATION.md` | API endpoints reference |

---

## 🎓 Teaching Use Cases

### 1. Test Different Restaurant Configurations
Modify business_info.csv (hours, menu, capacity) and see how AI adapts

### 2. Demonstrate Document-Based Prompting
Show how CSV data → system prompt → AI behavior (no code changes)

### 3. Test LLM Behavior Variations
Same AI model, different CSV data = different behavior

### 4. Learn CSV-Based Persistence
Understand how data persists across server restarts

### 5. Practice Concurrent Booking Logic
Multiple users → CSV concurrent writes → validate no overbooking

### 6. Build DeepEval Test Suite
Create comprehensive tests for AI reservation accuracy

---

## 💾 File Structure

```
restaurant ai model/
├── backend/
│   ├── main.py                    # 🐍 FastAPI backend
│   ├── business_info.csv          # 📊 Knowledge base
│   ├── reservations.csv           # 📋 Bookings (auto-created)
│   ├── Dockerfile                 # 🐳 Container config
│   └── requirements.txt            # Dependencies
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx                # 🎨 Main component
│   │   ├── App.css                # Styling
│   │   └── main.jsx               # Entry point
│   ├── package.json               # NPM dependencies
│   ├── vite.config.js             # Vite config
│   └── Dockerfile                 # Container config
│
├── tests/
│   ├── conftest.py                # Test fixtures
│   └── test_restaurant_assistant.py # Unit tests
│
├── CSV_QUICK_START.md             # Quick reference
├── CSV_KNOWLEDGE_BASE.md          # Full CSV docs
├── CSV_DEMONSTRATION.md           # Testing scenarios
├── README.md                       # Project overview
├── ARCHITECTURE.md                # System design
├── API_DOCUMENTATION.md           # API reference
├── CONTRIBUTING.md                # Development guide
├── DEEPEVAL_GUIDE.md              # Testing framework
├── QUICKSTART.md                  # Setup instructions
└── docker-compose.yml             # Multi-container setup
```

---

## ✨ What Makes This Special

### For Developers
✅ **No Hardcoding** - All data in CSVs  
✅ **Easy Testing** - Modify data, run tests, verify results  
✅ **Git-Friendly** - CSVs are versionable  
✅ **Scalable** - Easy to add new dishes, tables, rules  

### For AI/ML Students
✅ **Real-World Example** - How LLMs work with data  
✅ **RAG Pattern** - Retrieval-Augmented Generation  
✅ **Prompt Engineering** - Dynamic system prompts  
✅ **Data-Driven AI** - Behavior from data, not code  

### For Beginners
✅ **Simple to Understand** - No complex architecture  
✅ **Easy to Modify** - Just edit CSVs, no Python knowledge needed  
✅ **Clear Data Flow** - CSV → Prompt → AI → CSV  
✅ **Beautiful UI** - Professional-looking frontend  

---

## 🚀 Next Steps

1. **Explore the CSVs** - See how data flows
2. **Modify business_info.csv** - Add dishes, change hours
3. **Test the API** - Use curl to verify changes
4. **Try the Frontend** - Book through the web interface
5. **Set Up Tests** - Create DeepEval test suite
6. **Deploy** - Use `docker-compose up` to run everything

---

## 🎯 Summary

You now have a **complete, production-ready AI restaurant system** that:

✅ Uses **CSV files as the knowledge base**  
✅ Answers questions **based on CSV data**  
✅ Books reservations **with CSV persistence**  
✅ Validates rules **from CSV policies**  
✅ Customizable **without code changes**  
✅ Perfect for **teaching document-based prompting**  

**All in about 300 lines of Python + React!** 🎉

---

## 📖 Learn More

- See `CSV_QUICK_START.md` for quick examples
- See `CSV_KNOWLEDGE_BASE.md` for complete documentation
- See `CSV_DEMONSTRATION.md` for testing scenarios
- See `DEEPEVAL_GUIDE.md` for testing framework setup

---

**Congratulations! Your AI restaurant system is ready to go!** 🍝🤖✨
