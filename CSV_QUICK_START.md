# 🚀 QUICK START: CSV-Based AI Restaurant System

## What You Just Got

A **complete restaurant reservation AI** that uses CSV files as the knowledge base:
- ✅ **business_info.csv** - Restaurant details, menu, tables, policies
- ✅ **reservations.csv** - All bookings automatically saved
- ✅ **FastAPI backend** - Loads CSVs, answers questions, books tables
- ✅ **React frontend** - Beautiful Italian restaurant website
- ✅ **Ollama integration** - Local AI model (no API costs!)

---

## 🎯 How It Works

```
User Message
    ↓
Backend /chat API
    ↓
Loads business_info.csv → Builds system prompt
Loads reservations.csv → Current availability
    ↓
Ollama AI (Gemma 3 4B) → Generates response
    ↓
Validates reservation rules from CSV
    ↓
Saves to reservations.csv
    ↓
Returns to Frontend
```

---

## 📊 CSV Files Explained

### business_info.csv - The Knowledge Base
Contains ALL information about your restaurant that the AI reads:

```
key                | value                                  | category
name              | Bella Italia                           | restaurant
open_hour         | 11                                     | operations
close_hour        | 22                                     | operations
dish_1            | Bruschetta al Pomodoro|Appetizers|$8|...| menu
table_1           | Table 1 (Cozy Corner)|2                | tables
policy_1          | Only accept reservations 11AM-10PM     | policies
vegetarian_options| Mozzarella di Bufala|Bruschetta|...    | dietary
```

### reservations.csv - The Bookings
Auto-created on first run, appended to on each booking:

```
table_id | date      | time_start | time_end | party_size | name | dishes                    | created_at
4        | 2026-07-29| 19:00      | 21:00    | 4          | Guest| Margherita, Tiramisu      | 2026-07-28T20:11:38...
7        | 2026-07-29| 20:00      | 22:00    | 6          | Guest| Spaghetti al Carbonara... | 2026-07-28T04:21:58...
```

---

## 🎨 How to Customize

### Example 1: Change Restaurant Hours

**File:** `backend/business_info.csv`

**Current:**
```
open_hour,11,operations
close_hour,22,operations
```

**Change to:**
```
open_hour,10,operations
close_hour,23,operations
```

**Result:** AI will now book from 10 AM to 11 PM ✅

---

### Example 2: Add New Dish

**File:** `backend/business_info.csv`

**Add this row:**
```
dish_14,Risotto ai Funghi|Pasta & Risotto|$17|Creamy wild mushroom risotto,menu
```

**Then add to vegetarian options:**
```
vegetarian_options,Mozzarella di Bufala|Bruschetta al Pomodoro|Margherita|Risotto ai Funghi|Panna Cotta|Gelato Trio,dietary
```

**Result:** Next time user asks about vegetarian options OR says "risotto", AI will recognize it ✅

---

### Example 3: Change Max Party Size

**File:** `backend/business_info.csv`

**Current:**
```
max_party_size,8,operations
```

**Change to:**
```
max_party_size,10,operations
```

**Result:** AI will accept parties up to 10 people ✅

---

### Example 4: Add New Policy

**File:** `backend/business_info.csv`

**Add:**
```
policy_6,Groups of 8+ require 48 hours notice,policies
```

**Result:** AI will mention this policy when booking large groups ✅

---

## 📈 Testing the System

### Test 1: Q&A From Business CSV
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your hours? Do you have vegetarian options?"}'
```

**Expected:** AI answers using data from business_info.csv ✅

---

### Test 2: Booking & CSV Persistence
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book 4 people tomorrow at 7 PM for margherita and tiramisu"}'
```

**Expected:** 
- AI confirms reservation with table number ✅
- Data saved to reservations.csv ✅

---

### Test 3: Verify CSV Data

```bash
curl http://localhost:8000/reservations | python3 -m json.tool
```

**Expected:** See all bookings with dishes, dates, times ✅

---

## 🔄 Workflow: Modify → Test → Verify

### Step 1: Modify business_info.csv
Edit `backend/business_info.csv` in VS Code

### Step 2: Restart Backend
Kill and restart the backend to reload CSV data:
```bash
# Backend terminal: Ctrl+C to stop
# Then restart:
python3 main.py
```

### Step 3: Test with Frontend or API
- Open http://localhost:5174 in browser
- Try the "Reserve" section chatbot
- Or use curl to test API

### Step 4: Verify Data
```bash
# Check if booking was saved
curl http://localhost:8000/reservations | python3 -m json.tool

# Or view CSV directly
cat backend/reservations.csv
```

---

## 🧪 Teaching Examples

### Example A: Test Configuration Changes
**Task:** "What if we only serve lunch (11 AM - 3 PM)?"

1. Edit business_info.csv:
   ```
   close_hour,15,operations  # Change from 22 to 15
   ```

2. Restart backend

3. Try booking at 8 PM:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -d '{"message": "Book table for 4 at 8 PM tomorrow"}'
   ```

4. Result: AI rejects booking (outside hours) ✅

**Teaching Point:** AI behavior is 100% data-driven from CSV, no code changes needed!

---

### Example B: Test Menu Recognition
**Task:** "Add new dish and see if AI recognizes it"

1. Add to business_info.csv:
   ```
   dish_14,Pappardelle ai Funghi|Pasta|$17|Wild mushroom pasta,menu
   ```

2. Restart backend

3. User message: "I want pappardelle with mushrooms"
   ```bash
   curl -X POST http://localhost:8000/chat \
     -d '{"message": "Book 2 people tomorrow at 7 PM. I want pappardelle with mushrooms"}'
   ```

4. Result: AI recognizes "pappardelle", includes in reservation ✅

**Teaching Point:** Dish recognition is keyword-based from CSV menu list

---

### Example C: Test Business Rules
**Task:** "What if max party size was 5 instead of 8?"

1. Edit business_info.csv:
   ```
   max_party_size,5,operations
   ```

2. Restart backend

3. Try booking 6 people:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -d '{"message": "Book 6 people tomorrow at 7 PM"}'
   ```

4. Result: AI rejects (exceeds max party size) ✅

**Teaching Point:** All business logic comes from CSV configuration

---

## 📁 File Structure

```
backend/
├── main.py                      # 🐍 FastAPI backend (loads CSVs)
├── business_info.csv            # 📊 Knowledge base (restaurant info, menu, policies)
├── reservations.csv             # 📋 Bookings (auto-created & updated)
└── requirements.txt

frontend/
├── src/
│   ├── App.jsx                  # 🎨 React component
│   └── App.css                  # 🎨 Styling
└── package.json

CSV_KNOWLEDGE_BASE.md            # 📖 Full documentation
```

---

## ✨ Key Features

### For Users
- 🎯 Book tables via AI chatbot
- 📱 Responsive web interface
- 🍝 Browse Italian menu
- ❓ Ask questions about restaurant
- 🥗 Dietary preference recommendations

### For Developers
- 📊 Document-based prompting with CSVs
- 🔄 No-code customization
- 📈 Easy to test LLM behavior
- 🚀 Ready for DeepEval testing
- 💾 Persistent data in human-readable CSV format
- 🤖 Local AI (Ollama) - no cloud API costs

### For Teaching
- ✅ Perfect LLM testing example
- ✅ Shows data-driven AI development
- ✅ Demonstrates REST APIs
- ✅ Real-world reservation system logic
- ✅ Easy to modify and test variations

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| AI doesn't recognize new dishes | Restart backend after editing CSV |
| Restaurant hours not changing | Edit `open_hour` & `close_hour` in CSV, restart |
| Bookings not saving | Check reservations.csv exists and is writable |
| Port 8000 already in use | Kill process: `lsof -i :8000 \| grep -v COMMAND \| awk '{print $2}' \| xargs kill -9` |
| Frontend can't reach backend | Verify backend running on port 8000, check CORS settings |

---

## 🎓 Next Steps

1. **Explore the CSV files** - See how data flows to AI
2. **Modify business_info.csv** - Add dishes, change hours
3. **Test the API** - Use curl to verify changes
4. **Run tests** - `python3 -m pytest tests/`
5. **Set up DeepEval** - Test AI responses systematically
6. **Deploy** - Use Docker: `docker-compose up`

---

## 💡 Pro Tips

✅ **Do This:**
- Edit CSV files directly for customization
- Use `GET /reservations` to verify bookings
- Restart backend after CSV changes
- Test with API before frontend

❌ **Don't Do This:**
- Hardcode business info in Python
- Delete CSV headers
- Use commas in CSV values without escaping
- Directly edit reservations.csv while app is running

---

## 📞 API Reference

### POST /chat - Book tables or ask questions
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book 4 people tomorrow at 7 PM"}'
```

### GET /reservations - View all bookings
```bash
curl http://localhost:8000/reservations
```

### GET / - Health check
```bash
curl http://localhost:8000/
```

---

## 🎉 Summary

You now have a **complete AI restaurant system** with:
- ✅ CSV knowledge base (business_info.csv)
- ✅ CSV reservations (reservations.csv)
- ✅ AI model (Ollama Gemma 3 4B)
- ✅ REST API (FastAPI)
- ✅ Web interface (React)
- ✅ Zero cloud costs (local AI)
- ✅ Full customizability (just edit CSVs!)

**Perfect for teaching document-based LLM prompting!** 🚀
