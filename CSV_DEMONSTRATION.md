# 🎬 Live Demonstration: CSV-Based AI Testing

## Scenario 1: Test Menu Changes

### Step 1: Add New Dish to business_info.csv
Current menu has 13 dishes. Let's add a 14th specialty dish.

**Edit:** `backend/business_info.csv`

**Add this line:**
```
dish_14,Risotto ai Tartufi|Pasta & Risotto|$32|Black truffle risotto with truffle oil and shaved parmesan,menu
```

**Also update:**
```
specialty_6,Risotto ai Tartufi,specialties
```

### Step 2: Restart Backend
```bash
# In backend terminal: Ctrl+C
# Then run again:
python3 main.py
```

### Step 3: Test AI Recognition
Ask about the new dish:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Do you have any truffle dishes? I want to book for 2 people tomorrow at 8 PM with truffle risotto"}'
```

### Expected Result ✅
- AI mentions the new dish in its response
- Reservation includes "Risotto ai Tartufi" in dishes
- All without ANY code changes - pure CSV customization!

---

## Scenario 2: Test Business Hours Changes

### Step 1: Change Hours
**Edit:** `backend/business_info.csv`

**Change from:**
```
open_hour,11,operations
close_hour,22,operations
```

**Change to:**
```
open_hour,12,operations
close_hour,23,operations
```

### Step 2: Restart Backend
```bash
python3 main.py
```

### Step 3: Test Old vs New Hours

**Try booking at 11:00 AM (should fail):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book table for 4 at 11 AM tomorrow"}'
```

**Try booking at 12:00 PM (should work):**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book table for 4 at 12 PM tomorrow"}'
```

### Expected Result ✅
- 11 AM booking rejected (outside hours)
- 12 PM booking confirmed (within new hours)
- AI uses exact hours from CSV

---

## Scenario 3: Test Capacity Changes

### Step 1: Create Premium Table
**Edit:** `backend/business_info.csv`

**Add:**
```
table_11,Table 11 (VIP Chef's Table)|3,tables
```

**Also add:**
```
max_party_size,11,operations
```

### Step 2: Restart Backend

### Step 3: Test Booking at New Table
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book table for 3 people tomorrow at 9 PM"}'
```

### Expected Result ✅
- System suggests Table 11 (new VIP table)
- Works seamlessly without code changes
- Pure CSV-driven configuration

---

## Scenario 4: Test Dietary Restrictions

### Step 1: Add Dietary Category
**Edit:** `backend/business_info.csv`

**Add:**
```
gluten_free_options,Margherita|Osso Buco with Risotto|Panna Cotta|Gelato Trio,dietary
```

### Step 2: Restart Backend

### Step 3: Test Dietary Query
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I am gluten free. What can I eat? Book for 2 tomorrow at 7 PM"}'
```

### Expected Result ✅
- AI lists gluten-free options from CSV
- Booking includes dietary preference info
- Shows how easily we can handle dietary data

---

## Scenario 5: Complex: Change Multiple Settings

### Edit business_info.csv with:
```
name,Bella Italia Premium,restaurant
open_hour,12,operations
close_hour,23,operations
max_party_size,6,operations
```

### Add new policies:
```
policy_6,Minimum party size is 2 people,policies
policy_7,Advance reservations required,policies
```

### Restart backend and test:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your restaurant called? What are your policies?"}'
```

### Expected Result ✅
- AI responds with NEW name
- Lists NEW policies from CSV
- Everything updated without code changes

---

## Data Flow Visualization

```
CSV Files (Knowledge Base)
├── business_info.csv
│   ├── Restaurant name, address, phone
│   ├── Business hours (open_hour, close_hour)
│   ├── Menu items (dish_1-dish_N)
│   ├── Tables (table_1-table_10)
│   ├── Specialties
│   ├── Policies
│   └── Dietary options
│
└── reservations.csv
    ├── Previous bookings
    ├── Table availability
    └── Dish selections

        ↓ [Backend loads on startup]

System Prompt Generation
├── Restaurant Info
├── Menu (from CSV)
├── Available Tables (from CSV)
├── Current Reservations (from CSV)
├── Business Rules (from CSV)
└── Policies (from CSV)

        ↓ [Sent to Ollama]

LLM Response
├── Answers questions using CSV data
├── Validates reservations using CSV rules
└── Extracts dishes recognized in CSV

        ↓ [Post-processing]

Database Update
└── Save booking to reservations.csv
```

---

## Test Suite Ideas for DeepEval

### Test 1: Menu Item Recognition
```python
def test_ai_recognizes_menu_items():
    message = "I want carbonara and tiramisu"
    response = chat(message)
    assert "Spaghetti al Carbonara" in response
    assert "Tiramisu" in response
```

### Test 2: Availability Checking
```python
def test_no_double_booking():
    # Book table 7 for tomorrow 8-10 PM
    booking1 = chat("Book table for 6 tomorrow at 8 PM")
    
    # Try to book same table overlapping time
    booking2 = chat("Book table for 6 tomorrow at 9 PM")
    
    # Second booking should fail
    assert "available" not in booking2.lower()
```

### Test 3: Business Hours Validation
```python
def test_respects_business_hours():
    message = "Book table for 4 at 2 AM tomorrow"
    response = chat(message)
    assert "outside business hours" in response.lower()
```

### Test 4: Dietary Recommendations
```python
def test_suggests_vegetarian_options():
    message = "I'm vegetarian. What can I eat?"
    response = chat(message)
    
    # Should mention items from CSV
    assert "Margherita" in response
    assert "Mozzarella" in response or "mozzarella" in response
```

### Test 5: Data Persistence
```python
def test_reservations_persisted():
    # Make booking
    response1 = chat("Book 4 people tomorrow at 7 PM")
    
    # Restart backend
    restart_backend()
    
    # Check reservation still exists
    reservations = get_reservations()
    assert len(reservations) > 0
```

---

## Advanced: Bulk Testing Different Configurations

### Test Script
```bash
#!/bin/bash

# Save original CSV
cp backend/business_info.csv backup_business_info.csv

# Test 1: Small restaurant (2 tables)
sed -i 's/table_count,10/table_count,2/' backend/business_info.csv
python3 backend/main.py &
sleep 2
curl -X POST http://localhost:8000/chat -d '{"message": "Book table for 10 people"}'
kill %1

# Test 2: Late night hours (10 PM - 3 AM)
sed -i 's/close_hour,22/close_hour,3/' backup_business_info.csv
sed -i 's/open_hour,11/open_hour,22/' backup_business_info.csv
cp backup_business_info.csv backend/business_info.csv
python3 backend/main.py &
sleep 2
curl -X POST http://localhost:8000/chat -d '{"message": "Book table for 4 at 2 AM"}'
kill %1

# Test 3: Expensive restaurant (high prices)
# ... and so on ...

# Restore
mv backup_business_info.csv backend/business_info.csv
```

---

## Performance Testing

### Test: How many reservations can we handle?

```bash
#!/bin/bash

# Create 100 reservations
for i in {1..100}; do
    time_hour=$((11 + (i % 11)))
    table=$((1 + (i % 10)))
    
    curl -X POST http://localhost:8000/chat \
      -H "Content-Type: application/json" \
      -d "{\"message\": \"Book table for 4 at $time_hour:00\"}"
done

# Check final count
curl http://localhost:8000/reservations | grep total_reservations
```

### Expected: Should handle 100+ bookings smoothly ✅

---

## Summary: Why This Matters

### For Development
- ✅ Zero code changes to test different configurations
- ✅ CSV files are human-readable and editable
- ✅ Easy to rollback changes
- ✅ Version control friendly (CSVs in git)

### For Testing
- ✅ Test AI behavior with different rule sets
- ✅ Measure how well LLM follows CSV constraints
- ✅ Compare responses with different data
- ✅ Validate data persistence

### For Deployment
- ✅ Change restaurant info without redeploying
- ✅ Add new dishes without code updates
- ✅ Modify policies on the fly
- ✅ Scale reservations without database migration

### For Teaching
- ✅ Show students how AI systems use data
- ✅ Demonstrate RAG (Retrieval-Augmented Generation)
- ✅ Explain prompt engineering with real data
- ✅ Practice test-driven AI development

---

**This is the power of document-based prompting!** 📊🚀
