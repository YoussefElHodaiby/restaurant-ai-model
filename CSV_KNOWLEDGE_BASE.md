# 📋 CSV Knowledge Base System Documentation

## Overview

The Restaurant AI Assistant now uses **CSV files as the primary knowledge base** for all business information and reservations. This approach provides:

✅ **Document-Based Prompting** - All AI knowledge comes from data files, not hardcoded values  
✅ **Easy Customization** - Modify restaurant info without changing code  
✅ **Persistent Reservations** - All bookings automatically saved to CSV  
✅ **Perfect for Teaching** - Demonstrates real-world LLM data integration patterns  

---

## CSV Files Overview

### 1. **business_info.csv** - Restaurant Knowledge Base
This file contains ALL business information that the AI model reads to answer questions.

**Columns:**
- `key` - Information identifier (e.g., "name", "open_hour", "dish_1")
- `value` - The actual value (e.g., "Bella Italia", "11", "Bruschetta al Pomodoro|Appetizers|$8|...")
- `category` - Organizational category (restaurant, operations, contact, menu, tables, specialties, dietary, policies)
- `notes` - Description of the entry

**Categories:**

#### Restaurant Info
```
key         | value                                      | category
name        | Bella Italia                              | restaurant
cuisine     | Italian                                   | restaurant
description | Authentic Italian Cuisine • Family...     | restaurant
```

#### Contact Information
```
key     | value                              | category
address | 123 Italian Street New York NY...  | contact
phone   | (555) 123-4567                    | contact
email   | info@bellaitalia.com              | contact
```

#### Operations
```
key                 | value | category
hours              | 11 AM - 10 PM            | operations
open_hour          | 11                       | operations
close_hour         | 22                       | operations
max_duration_hours | 2                        | operations
max_party_size     | 8                        | operations
table_count        | 10                       | operations
```

#### Menu Items
Each dish follows the format: `Name|Category|Price|Description`

```
key     | value                                                    | category
dish_1  | Bruschetta al Pomodoro|Appetizers|$8|Toasted bread...  | menu
dish_2  | Calamari Fritti|Appetizers|$12|Golden fried squid...  | menu
dish_4  | Spaghetti al Carbonara|Pasta & Risotto|$16|Classic...  | menu
```

#### Tables
Each table follows the format: `Name|Capacity`

```
key     | value                           | category
table_1 | Table 1 (Cozy Corner)|2        | tables
table_4 | Table 4 (Family)|4             | tables
table_10| Table 10 (Private)|8           | tables
```

#### Specialties
```
key         | value                    | category
specialty_1 | Spaghetti al Carbonara   | specialties
specialty_2 | Pappardelle al Ragù      | specialties
specialty_3 | Osso Buco with Risotto   | specialties
```

#### Policies
```
key        | value                                    | category
policy_1   | Only accept reservations between...     | policies
policy_2   | Each reservation is limited to 2 hours  | policies
policy_3   | Never book the same table...            | policies
```

#### Dietary Information
```
key                 | value                                    | category
vegetarian_options  | Mozzarella di Bufala|Bruschetta|...     | dietary
```

### 2. **reservations.csv** - Booking Records
This file automatically stores all customer reservations.

**Columns:**
- `table_id` - Table number (1-10)
- `date` - Reservation date (YYYY-MM-DD format)
- `time_start` - Start time (HH:MM 24-hour format)
- `time_end` - End time (HH:MM 24-hour format)
- `party_size` - Number of people
- `name` - Customer name
- `dishes` - Comma-separated dish names ordered
- `created_at` - ISO timestamp when reservation was made

**Example:**
```
table_id,date,time_start,time_end,party_size,name,dishes,created_at
7,2026-07-29,20:00,22:00,6,Guest,"Spaghetti al Carbonara, Tiramisu",2026-07-28T04:21:58.895006
4,2026-07-29,19:00,21:00,4,Guest,"Margherita, Panna Cotta",2026-07-28T10:30:45.123456
```

---

## How the System Works

### 1. Backend Startup Process
```
1. main.py starts
2. Loads business_info.csv into BUSINESS_DATA dictionary
3. Loads reservations.csv into reservations list
4. When user sends a message:
   - Extracts reservation details from message
   - Extracts dish names from message
   - Calls get_system_prompt() to build AI prompt from CSV data
   - Sends prompt + message to Ollama
   - Validates reservation and saves to CSV if valid
```

### 2. System Prompt Generation
The AI system prompt is **completely dynamic** and built from CSV files:

```python
def get_system_prompt():
    # Load latest restaurant info from business_info.csv
    restaurant_info = get_restaurant_info()
    
    # Build menu from CSV menu items
    menu_info = "FULL MENU:\n\n"
    for dish in CSV_menu_data:
        menu_info += f"  • {dish['name']} ({dish['price']}) - {dish['description']}\n"
    
    # Include current reservations from reservations.csv
    current_reservations = "CURRENT RESERVATIONS:\n"
    for booking in reservations:
        current_reservations += f"- Table {booking['table_id']}: ..."
    
    # Build from policies, dietary info, tables, etc.
    # Return complete system prompt with ALL info from CSVs
```

### 3. Reservation Validation & Persistence
```
When user says "Book table for 4 people tomorrow at 7 PM":

1. Extract details: party_size=4, date=tomorrow, time=19:00
2. Check against CSV rules:
   - Is 19:00 within open_hour(11) to close_hour(22)? ✓
   - Is party_size(4) ≤ max_party_size(8)? ✓
   - Is there an available table? Check against reservations.csv
3. If valid:
   - Create reservation dict
   - Append to reservations.csv file
   - Return confirmation with table number
4. If invalid:
   - Suggest alternatives based on CSV availability
```

---

## How to Customize the System

### Modify Restaurant Hours
Edit `business_info.csv`:
```
open_hour,9,operations    # Change from 11 to 9
close_hour,23,operations  # Change from 22 to 23
```
→ AI will automatically use new hours on next request

### Add New Dishes
Edit `business_info.csv` and add:
```
dish_14,Risotto ai Funghi|Pasta & Risotto|$17|Creamy mushroom risotto,menu
```
→ AI will include it in menu and recognize it in customer messages

### Change Table Capacity
Edit `business_info.csv`:
```
table_7,Table 7 (Large Group)|8,tables    # Change from 6 to 8
```
→ AI will use new capacity for availability checking

### Update Restaurant Name/Address
Edit `business_info.csv`:
```
name,My Restaurant Name,restaurant
address,New Address Here,contact
```
→ All AI responses will use new info

### Add Dietary Restrictions
Edit `business_info.csv`:
```
gluten_free_options,Bruschetta|Margherita|Panna Cotta,dietary
vegan_options,Bruschetta|Margherita,dietary
```
→ AI can answer dietary questions from CSV

---

## API Endpoints

### 1. POST /chat - Chat with AI
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Book table for 4 people tomorrow at 7 PM"}'
```

**Response:**
```json
{
  "reply": "✅ [RESERVATION CONFIRMED - Table 4 (Family) has been reserved for 4 people on 2026-07-29 at 19:00 for 2 hours]"
}
```

### 2. GET /reservations - View All Bookings
```bash
curl http://localhost:8000/reservations
```

**Response:**
```json
{
  "total_reservations": 2,
  "reservations": [
    {
      "table_id": 7,
      "date": "2026-07-29",
      "time_start": "20:00",
      "time_end": "22:00",
      "party_size": 6,
      "name": "Guest",
      "dishes": "Spaghetti al Carbonara, Tiramisu",
      "created_at": "2026-07-28T04:21:58.895006"
    }
  ]
}
```

---

## Teaching Use Cases

### 1. Test Different Restaurant Configurations
**Scenario:** "What if we had different hours?"
- Modify `open_hour` and `close_hour` in business_info.csv
- No code changes needed
- See how AI responds differently
- Perfect for testing without recompilation

### 2. Test Menu Changes
**Scenario:** "How does the AI adapt to new menu items?"
- Add `dish_14`, `dish_15` to business_info.csv
- Test if AI recognizes new dishes in customer messages
- Verify CSV data flows through to system prompt

### 3. Test Reservation Logic with Different Rules
**Scenario:** "What if max party size was 6 instead of 8?"
- Change `max_party_size` in business_info.csv
- Test how AI validates reservations
- See how it handles oversized parties

### 4. Demonstrate Document-Based Prompting
**Scenario:** "How can we build AI behavior from data files?"
- Show how business_info.csv → system prompt → AI behavior
- Explain that NO hardcoded business logic exists in Python
- All rules are in CSV, making it data-driven

### 5. Test Concurrency & CSV Atomicity
**Scenario:** "Can multiple users book simultaneously?"
- Have multiple browsers send requests
- Check reservations.csv for conflicts
- Verify no double-booking occurs
- Great for testing concurrent CSV writes

---

## File Structure
```
backend/
├── main.py                 # FastAPI backend (loads CSVs)
├── business_info.csv       # 📊 Restaurant knowledge base
├── reservations.csv        # 📋 Booking records (auto-generated)
└── requirements.txt        # Python dependencies

frontend/
├── src/App.jsx            # React frontend
└── ...

tests/
└── test_restaurant_assistant.py  # Unit tests
```

---

## Best Practices

### ✅ DO:
- Edit CSV files directly to customize the system
- Use `GET /reservations` to verify bookings are saved
- Test CSV loading by restarting the backend
- Use structured format for menu items: `Name|Category|Price|Description`
- Keep table capacity realistic (2-8 people)
- Use 24-hour format for times (11:00-22:00)

### ❌ DON'T:
- Hardcode business info in Python - use CSV instead
- Delete column headers in CSV files
- Use commas in CSV values without proper escaping
- Change table_id after making reservations
- Remove existing reservations.csv rows (append-only)

---

## Example CSV Modifications

### Add a new policy
```
policy_6,Accept both cash and credit cards,policies
```

### Change restaurant hours to include lunch service
```
hours,10 AM - 11 PM (Monday - Sunday),operations
open_hour,10,operations
```

### Add a premium table
```
table_11,VIP Table (Chef's Table)|2,tables
```

### Add vegetarian pasta option
```
dish_14,Pappardelle ai Funghi|Pasta & Risotto|$17|Wild mushroom pasta (vegetarian),menu
vegetarian_options,Mozzarella di Bufala|Bruschetta al Pomodoro|Margherita|Pappardelle ai Funghi|Panna Cotta|Gelato Trio,dietary
```

---

## Troubleshooting

### AI doesn't recognize new dishes
**Solution:** Ensure `dish_N` key is in business_info.csv and backend reloaded

### Restaurant hours not changing
**Solution:** Modify `open_hour` and `close_hour` in CSV, restart backend with `python3 main.py`

### Reservations not saved
**Solution:** Check reservations.csv exists and is writable, verify `/reservations` endpoint returns bookings

### CSV parsing errors
**Solution:** Ensure no unescaped commas in values, check all rows have correct number of columns

---

## Summary

The **CSV Knowledge Base System** makes this restaurant AI application:
- **Data-driven** - All business logic in CSV files
- **No-code customizable** - Change behavior without Python editing  
- **Educational** - Perfect for teaching document-based prompting
- **Production-ready** - Persistent CSV storage, full API
- **LLM agnostic** - Works with any LLM (Ollama, OpenAI, Claude, etc.)

All information the AI uses comes from `business_info.csv` and `reservations.csv` - no hardcoding, no code changes needed! 🎉
