"""
Restaurant AI Reservation Assistant
FastAPI backend for chatbot interface
Using Groq API (Cloud-based LLM)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
import re
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sys

try:
    import psycopg2
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False

# Load environment variables
load_dotenv()

# Database config (set DATABASE_URL in Vercel env vars to use PostgreSQL)
DATABASE_URL = os.getenv("DATABASE_URL")
USE_DATABASE = bool(DATABASE_URL and PSYCOPG2_AVAILABLE)

# Groq API Configuration
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")  # Set GROQ_API_KEY in your .env or Vercel environment variables
GROQ_MODEL = "llama-3.3-70b-versatile"  # Latest Groq Llama model

app = FastAPI(title="Restaurant AI Assistant")

# Enable CORS for React frontend
_extra_origins = [o for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", "http://localhost:5174", "http://localhost:5175",
        "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        *_extra_origins,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware to debug requests
@app.middleware("http")
async def log_requests(request, call_next):
    print(f"[FASTAPI] {request.method} {request.url.path}", file=sys.stderr, flush=True)
    response = await call_next(request)
    return response

# CSV files for data storage — use absolute paths so they resolve correctly on Vercel
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESERVATIONS_CSV = os.path.join(_BASE_DIR, "reservations.csv")
BUSINESS_INFO_CSV = os.path.join(_BASE_DIR, "business_info.csv")
CSV_HEADERS = ["table_id", "date", "time_start", "time_end", "party_size", "name", "dishes", "created_at"]

# Initialize CSV files if they don't exist
def init_csv_files():
    """Initialize CSV files with headers if they don't exist"""
    if USE_DATABASE:
        return  # PostgreSQL handles persistence; no CSV needed
    if not os.path.exists(RESERVATIONS_CSV):
        try:
            with open(RESERVATIONS_CSV, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(CSV_HEADERS)
        except OSError:
            pass  # Read-only filesystem (e.g. Vercel) – skip gracefully
    if not os.path.exists(BUSINESS_INFO_CSV):
        print(f"⚠️  {BUSINESS_INFO_CSV} not found. Please ensure it exists with business information.")

init_csv_files()

# In-memory reservation storage (loaded from CSV at startup)
reservations = []

def load_reservations_from_csv():
    """Load all reservations — from PostgreSQL if DATABASE_URL is set, else CSV"""
    global reservations
    reservations = []
    if USE_DATABASE:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT table_id, date, time_start, time_end, party_size, name, dishes "
                    "FROM reservations ORDER BY date, time_start"
                )
                for row in cur.fetchall():
                    reservations.append({
                        'table_id': str(row[0]), 'date': row[1],
                        'time_start': row[2], 'time_end': row[3],
                        'party_size': str(row[4]), 'name': row[5],
                        'dishes': row[6] or 'Not specified'
                    })
            conn.close()
        except Exception as e:
            print(f"DB load error: {e}")
    else:
        try:
            with open(RESERVATIONS_CSV, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row:
                        reservations.append(row)
        except Exception as e:
            print(f"CSV load error: {e}")

def save_reservation_to_csv(reservation):
    """Save a reservation — to PostgreSQL if DATABASE_URL is set, else CSV"""
    if USE_DATABASE:
        try:
            conn = psycopg2.connect(DATABASE_URL)
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO reservations "
                    "(table_id, date, time_start, time_end, party_size, name, dishes) "
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (
                        reservation['table_id'], reservation['date'],
                        reservation['time_start'], reservation['time_end'],
                        reservation['party_size'], reservation['name'],
                        reservation['dishes']
                    )
                )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"DB save error: {e}")
    else:
        try:
            with open(RESERVATIONS_CSV, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
                writer.writerow(reservation)
        except Exception as e:
            print(f"CSV save error: {e}")

# Load existing reservations on startup
load_reservations_from_csv()


def load_business_info_from_csv():
    """Load restaurant business information from CSV file"""
    business_data = {}
    try:
        with open(BUSINESS_INFO_CSV, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and row.get('key'):
                    key = row['key']
                    value = row['value']
                    category = row.get('category', 'general')
                    
                    # Organize by category for easy access
                    if category not in business_data:
                        business_data[category] = {}
                    business_data[category][key] = value
    except Exception as e:
        print(f"Error loading business info CSV: {e}")
    return business_data


# Business data cache (reloaded on each request)
BUSINESS_DATA = load_business_info_from_csv()


def reload_business_info():
    """Reload business_info.csv into the global BUSINESS_DATA cache"""
    global BUSINESS_DATA
    BUSINESS_DATA = load_business_info_from_csv()


# Restaurant Information (loaded from CSV)
def get_restaurant_info():
    """Get restaurant info from the latest CSV data"""
    restaurant_info = BUSINESS_DATA.get('restaurant', {})
    operations = BUSINESS_DATA.get('operations', {})
    contact = BUSINESS_DATA.get('contact', {})
    menu = BUSINESS_DATA.get('menu', {})
    tables = BUSINESS_DATA.get('tables', {})
    specialties = BUSINESS_DATA.get('specialties', {})
    
    # Build tables list
    tables_list = []
    for i in range(1, 11):
        table_key = f'table_{i}'
        if table_key in tables:
            parts = tables[table_key].split('|')
            name = parts[0] if len(parts) > 0 else f"Table {i}"
            capacity = int(parts[1]) if len(parts) > 1 else 2
            tables_list.append({"id": i, "capacity": capacity, "name": name})
    
    # Build specialties list
    specialties_list = [v for k, v in sorted(specialties.items()) if k.startswith('specialty_')]
    
    return {
        "name": restaurant_info.get('name', 'Bella Italia'),
        "cuisine": restaurant_info.get('cuisine', 'Italian'),
        "description": restaurant_info.get('description', 'Authentic Italian Cuisine'),
        "address": contact.get('address', '123 Italian Street, New York, NY 10001'),
        "phone": contact.get('phone', '(555) 123-4567'),
        "email": contact.get('email', 'info@bellaitalia.com'),
        "hours": restaurant_info.get('hours', '11 AM - 10 PM'),
        "open_hour": int(operations.get('open_hour', 11)),
        "close_hour": int(operations.get('close_hour', 22)),
        "max_duration_hours": int(operations.get('max_duration_hours', 2)),
        "max_party_size": int(operations.get('max_party_size', 8)),
        "tables": tables_list,
        "specialties": specialties_list,
        "menu_items": menu
    }

# Initialize with CSV data
RESTAURANT_INFO = get_restaurant_info()
# NOTE: do NOT reset `reservations` here — it was already loaded from CSV above


def format_time_12hr(time_str: str) -> str:
    """Convert 24-hour time string (HH:MM) to 12-hour AM/PM display format"""
    hour, minute = map(int, time_str.split(":"))
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    if minute:
        return f"{display_hour}:{minute:02d} {period}"
    return f"{display_hour} {period}"


def extract_reservation_details(message: str):
    """
    Extract party size, date, and time from user message.
    Handles: 12-hour AM/PM, 24-hour format, noon/midnight,
    weekday names, month+day names, and numeric date formats.
    """
    details = {}
    message_lower = message.lower()

    # --- Party size ---
    party_patterns = [
        r'for\s+(\d+)\s+(?:people|persons?|guests?)',
        r'(\d+)\s+(?:people|persons?|guests?)',
        r'table\s+for\s+(\d+)',
        r'party\s+of\s+(\d+)',
        r'(\d+)\s+of\s+us',
    ]
    for pattern in party_patterns:
        match = re.search(pattern, message_lower)
        if match:
            details['party_size'] = int(match.group(1))
            break

    # --- Time ---
    # Special keywords
    if re.search(r'\bnoon\b', message_lower):
        details['time'] = "12:00"
    elif re.search(r'\bmidnight\b', message_lower):
        details['time'] = "00:00"
    else:
        # 1) HH:MM am/pm  e.g. "7:30 pm", "1:00am"
        match = re.search(r'\b(\d{1,2}):(\d{2})\s*(am|pm)\b', message_lower)
        if match:
            hour, minute, period = int(match.group(1)), int(match.group(2)), match.group(3)
            if 1 <= hour <= 12 and 0 <= minute <= 59:
                if period == 'pm' and hour != 12:
                    hour += 12
                elif period == 'am' and hour == 12:
                    hour = 0
                details['time'] = f"{hour:02d}:{minute:02d}"

        # 2) H am/pm  e.g. "7 pm", "1am"
        if 'time' not in details:
            match = re.search(r'\b(\d{1,2})\s*(am|pm)\b', message_lower)
            if match:
                hour, period = int(match.group(1)), match.group(2)
                if 1 <= hour <= 12:
                    if period == 'pm' and hour != 12:
                        hour += 12
                    elif period == 'am' and hour == 12:
                        hour = 0
                    details['time'] = f"{hour:02d}:00"

        # 3) 24-hour HH:MM  e.g. "19:00", "13:30"
        if 'time' not in details:
            match = re.search(r'\b([01]?\d|2[0-3]):([0-5]\d)\b', message_lower)
            if match:
                hour, minute = int(match.group(1)), int(match.group(2))
                details['time'] = f"{hour:02d}:{minute:02d}"

    # --- Date ---
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    if re.search(r'\btomorrow\b', message_lower):
        details['date'] = str(tomorrow)
    elif re.search(r'\b(today|tonight)\b', message_lower):
        details['date'] = str(today)
    else:
        # Weekday names: "Monday", "next Friday", "this Saturday"
        days_of_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for i, day_name in enumerate(days_of_week):
            if re.search(rf'\b(next\s+)?{day_name}\b', message_lower):
                days_ahead = (i - today.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Same weekday name = next week
                details['date'] = str(today + timedelta(days=days_ahead))
                break

        # Month name + day: "July 30", "July 30th", "30th of July", "30 July"
        if 'date' not in details:
            month_map = {
                'january': 1, 'jan': 1, 'february': 2, 'feb': 2,
                'march': 3, 'mar': 3, 'april': 4, 'apr': 4,
                'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
                'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'sept': 9,
                'october': 10, 'oct': 10, 'november': 11, 'nov': 11,
                'december': 12, 'dec': 12
            }
            month_pattern = '|'.join(month_map.keys())

            m = re.search(rf'\b({month_pattern})\s+(\d{{1,2}})(?:st|nd|rd|th)?\b', message_lower)
            if m:
                month_str, day = m.group(1), int(m.group(2))
            else:
                m = re.search(rf'\b(\d{{1,2}})(?:st|nd|rd|th)?(?:\s+of)?\s+({month_pattern})\b', message_lower)
                if m:
                    day, month_str = int(m.group(1)), m.group(2)
                else:
                    month_str, day = None, None

            if month_str and day is not None:
                month_num = month_map.get(month_str)
                if month_num:
                    try:
                        year = today.year
                        target = datetime(year, month_num, day).date()
                        if target < today:
                            target = datetime(year + 1, month_num, day).date()
                        details['date'] = str(target)
                    except ValueError:
                        pass

        # Numeric formats: MM/DD/YYYY, MM-DD-YYYY
        if 'date' not in details:
            m = re.search(r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b', message)
            if m:
                part1, part2, year = m.groups()
                year = '20' + year if len(year) == 2 else year
                try:
                    target = datetime(int(year), int(part1), int(part2)).date()
                    details['date'] = str(target)
                except ValueError:
                    pass

    return details if details else None


def extract_dishes_from_message(message):
    """
    Extract dish names from message if mentioned
    Returns a string of dish names
    """
    menu_items = {
        "bruschetta": "Bruschetta al Pomodoro",
        "calamari": "Calamari Fritti",
        "mozzarella": "Mozzarella di Bufala",
        "carbonara": "Spaghetti al Carbonara",
        "pappardelle": "Pappardelle al Ragù",
        "lasagna": "Lasagna della Nonna",
        "osso buco": "Osso Buco with Risotto",
        "margherita": "Margherita",
        "quattro formaggi": "Quattro Formaggi",
        "prosciutto": "Prosciutto e Rucola",
        "tiramisu": "Tiramisu",
        "panna cotta": "Panna Cotta",
        "gelato": "Gelato Trio"
    }
    
    found_dishes = []
    message_lower = message.lower()
    
    for keyword, dish_name in menu_items.items():
        if keyword in message_lower:
            if dish_name not in found_dishes:
                found_dishes.append(dish_name)
    
    return ", ".join(found_dishes) if found_dishes else ""


def create_reservation(party_size, date, time_str, table_id, customer_name="Guest", dishes=""):
    """
    Create a new reservation in the system
    Returns reservation details or error message
    """
    # Parse time and calculate end time
    hour, minute = map(int, time_str.split(":"))
    end_hour = hour + RESTAURANT_INFO['max_duration_hours']
    end_minute = minute
    
    if end_hour >= 24:
        end_hour = end_hour % 24
    
    end_time = f"{end_hour:02d}:{end_minute:02d}"
    
    # Create reservation
    reservation = {
        "table_id": table_id,
        "date": date,
        "time_start": time_str,
        "time_end": end_time,
        "party_size": party_size,
        "name": customer_name,
        "dishes": dishes if dishes else "Not specified",
        "created_at": datetime.now().isoformat()
    }
    
    reservations.append(reservation)
    
    # Save to CSV
    save_reservation_to_csv(reservation)
    
    return reservation


def is_table_available(table_id, date, start_time, end_time):
    """
    Check if a table is available for the given date and time range
    Prevents double-booking by checking overlap and exact duplicates
    """
    for reservation in reservations:
        # Convert table_id to int (CSV loads as strings)
        if int(reservation["table_id"]) != table_id or reservation["date"] != date:
            continue
        
        res_start = reservation["time_start"]
        res_end = reservation["time_end"]
        
        def time_to_minutes(time_str):
            h, m = map(int, time_str.split(":"))
            return h * 60 + m
        
        req_start_min = time_to_minutes(start_time)
        req_end_min = time_to_minutes(end_time)
        res_start_min = time_to_minutes(res_start)
        res_end_min = time_to_minutes(res_end)
        
        # Check for time overlap (prevents double-booking)
        if req_start_min < res_end_min and req_end_min > res_start_min:
            return False
    
    return True


def find_available_table(party_size, date, start_time, end_time):
    """
    Find the best available table for party size and time
    Returns table info or None if none available
    """
    # Sort tables by capacity (prefer smaller tables that fit)
    suitable_tables = [t for t in RESTAURANT_INFO["tables"] if t["capacity"] >= party_size]
    suitable_tables.sort(key=lambda x: x["capacity"])
    
    for table in suitable_tables:
        if is_table_available(table["id"], date, start_time, end_time):
            return table
    
    return None


def get_available_tables_summary(date, start_time, end_time):
    """
    Get a summary of available tables
    """
    available = []
    for table in RESTAURANT_INFO["tables"]:
        if is_table_available(table["id"], date, start_time, end_time):
            available.append(f"Table {table['id']} (capacity {table['capacity']})")
    return available

# Request model
class ChatMessage(BaseModel):
    message: str


# Response model
class ChatResponse(BaseModel):
    reply: str


def get_system_prompt():
    """Generate a SHORT, concise system prompt from CSV data"""
    
    restaurant_info = get_restaurant_info()
    today = datetime.now().date()
    
    # Show ALL reservations sorted by date → time → table so the LLM has full visibility
    if reservations:
        sorted_res = sorted(
            reservations,
            key=lambda r: (r['date'], r['time_start'], str(r['table_id']))
        )
        res_lines = [
            f"T{r['table_id']} | {r['date']} | {r['time_start']}-{r['time_end']} | {r['party_size']}p"
            for r in sorted_res
        ]
        current_reservations = "BOOKED SLOTS (T# | date | start-end | party):\n" + "\n".join(res_lines)
    else:
        current_reservations = "No reservations yet."
    
    # Compact menu - just list dishes with prices
    menu_list = []
    menu_items = restaurant_info.get('menu_items', {})
    for key in sorted(menu_items.keys())[:10]:  # First 10 dishes only
        parts = menu_items[key].split('|')
        if len(parts) >= 2:
            menu_list.append(f"{parts[0]} ({parts[2] if len(parts) > 2 else 'price'})")
    
    open_hr = restaurant_info['open_hour']
    close_hr = restaurant_info['close_hour']
    max_dur = restaurant_info['max_duration_hours']
    latest_start = f"{close_hr - max_dur}:00"
    open_display = format_time_12hr(f"{open_hr:02d}:00")
    close_display = format_time_12hr(f"{close_hr:02d}:00")
    latest_display = format_time_12hr(latest_start)

    # Contact & location
    address = restaurant_info.get('address', 'N/A')
    phone = restaurant_info.get('phone', 'N/A')
    email = restaurant_info.get('email', 'N/A')

    # Dietary options
    dietary_data = BUSINESS_DATA.get('dietary', {})
    veg = dietary_data.get('vegetarian_options', '').replace('|', ', ')

    # Payment policy
    policies = BUSINESS_DATA.get('policies', {})
    payment = policies.get('payment_policy', 'Cash and major credit cards')

    # Build compact table capacity summary
    tables_summary = " | ".join(
        f"T{t['id']}(capacity {t['capacity']})" for t in restaurant_info['tables']
    )

    return f"""You are {restaurant_info['name']} reservation assistant. ULTRA-SHORT replies only (1-2 sentences).

TODAY IS: {today} | Hours: {open_display}–{close_display} (last booking: {latest_display}) | Max party: {restaurant_info['max_party_size']}
Address: {address} | Phone: {phone} | Email: {email} | Payment: {payment}
ALWAYS confirm AM or PM. 1 PM = 13:00, 1 AM = 01:00. Each booking = 2-hour slot.

TABLE CAPACITIES (STRICTLY for seating, NEVER confuse table numbers with times):
{tables_summary}
CRITICAL: Table selection is based ONLY on capacity >= party size. NEVER pick a table whose number matches the booking hour or time. 2 PM does NOT mean Table 2. 7 PM does NOT mean Table 7. Always choose the smallest table whose capacity fits the party.

Menu: {', '.join(menu_list)}
Vegetarian options: {veg}

RULES: No double-booking. End time must be ≤ closing. Do NOT suggest a table number in your reply — the system will confirm the correct table automatically.

Current: {current_reservations}"""


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """
    Chat endpoint that processes user message through Groq API
    Now with proper reservation tracking
    """
    try:
        # Reload BOTH CSV files so every response reflects current data
        reload_business_info()
        load_reservations_from_csv()

        # Get system prompt with restaurant context
        system_prompt = get_system_prompt()
        
        # Extract reservation details from message
        reservation_details = extract_reservation_details(request.message)
        
        # Extract dishes from message
        dishes = extract_dishes_from_message(request.message)
        
        # Call Groq API with OpenAI-compatible format
        response = requests.post(
            GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": request.message
                    }
                ],
                "temperature": 0.5,
                "max_tokens": 150,  # Keep responses short and concise
                "top_p": 0.95
            },
            timeout=30
        )
        
        if response.status_code != 200:
            error_msg = response.json().get("error", {}).get("message", str(response.status_code))
            return ChatResponse(
                reply=f"Error from Groq API: {error_msg}"
            )
        
        data = response.json()
        assistant_reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
        
        if not assistant_reply:
            return ChatResponse(
                reply="No response from model. Please try again."
            )
        
        # Post-process the response to add reservation logic
        if reservation_details and all(k in reservation_details for k in ['party_size', 'date', 'time']):
            party_size = reservation_details['party_size']
            date = reservation_details['date']
            time_str = reservation_details['time']

            hour = int(time_str.split(":")[0])
            minute = int(time_str.split(":")[1])
            open_hour = RESTAURANT_INFO['open_hour']
            close_hour = RESTAURANT_INFO['close_hour']
            max_duration = RESTAURANT_INFO['max_duration_hours']

            req_start_min = hour * 60 + minute
            req_end_min = req_start_min + max_duration * 60
            open_min = open_hour * 60
            close_min = close_hour * 60
            latest_start_min = close_min - max_duration * 60
            latest_display = format_time_12hr(f"{latest_start_min // 60:02d}:{latest_start_min % 60:02d}")
            close_display = format_time_12hr(f"{close_hour:02d}:00")
            open_display = format_time_12hr(f"{open_hour:02d}:00")
            time_display = format_time_12hr(time_str)

            # Check business hours
            if req_start_min < open_min:
                assistant_reply = f"❌ We open at {open_display}. Please choose a time after {open_display}."
            elif req_end_min > close_min:
                assistant_reply = f"❌ Last booking is at {latest_display} (we close at {close_display}). Please choose an earlier time."
            # Check party size
            elif party_size > RESTAURANT_INFO['max_party_size']:
                assistant_reply = f"❌ Party size {party_size} exceeds our max of {RESTAURANT_INFO['max_party_size']}."
            else:
                # Validate date is not in the past
                today = datetime.now().date()
                try:
                    requested_date = datetime.strptime(date, "%Y-%m-%d").date()
                    if requested_date < today:
                        assistant_reply = f"❌ Cannot book in the past. {date} is before today ({today})."
                    else:
                        # Calculate end time (2-hour slot)
                        end_hour = hour + max_duration
                        end_time = f"{end_hour:02d}:{minute:02d}"
                        end_display = format_time_12hr(end_time)

                        # Find available table
                        available_table = find_available_table(party_size, date, time_str, end_time)

                        if available_table:
                            # Double-check no existing booking at exact time
                            existing = [r for r in reservations if int(r["table_id"]) == available_table['id'] and
                                        r["date"] == date and r["time_start"] == time_str]
                            if existing:
                                assistant_reply = (f"❌ Table {available_table['id']} is already booked on {date} "
                                                   f"at {time_display}. Please choose a different time or date.")
                            else:
                                reservation = create_reservation(party_size, date, time_str, available_table['id'],
                                                                 customer_name="Guest", dishes=dishes)
                                # Replace the LLM reply entirely with the authoritative confirmation
                                # so the LLM cannot suggest a wrong table number (e.g. confusing 2 PM → Table 2)
                                assistant_reply = (f"✅ CONFIRMED - Table {available_table['id']} "
                                                   f"(capacity {available_table['capacity']}) "
                                                   f"for {party_size} on {date} at {time_display} – {end_display}")
                                if dishes:
                                    assistant_reply += f" | Dishes: {dishes}"
                        else:
                            assistant_reply = (f"❌ No tables available for {party_size} people on {date} at "
                                               f"{time_display}. Please try a different time or date.")
                except ValueError:
                    assistant_reply = f"❌ Invalid date: {date}. Please use a format like 'July 30' or 'tomorrow'."
        
        return ChatResponse(reply=assistant_reply)
        
    except requests.exceptions.Timeout:
        return ChatResponse(
            reply="⚠️ Request timed out. Please try again."
        )
    except requests.exceptions.ConnectionError:
        return ChatResponse(
            reply="⚠️ Cannot connect to Groq API. Check your internet connection."
        )
    except requests.exceptions.RequestException as e:
        return ChatResponse(reply=f"⚠️ Error: {str(e)}")
    except Exception as e:
        return ChatResponse(reply=f"⚠️ An error occurred: {str(e)}")


@app.get("/reservations")
async def get_reservations():
    """Get all current reservations from CSV"""
    reload_business_info()          # Reload business info
    load_reservations_from_csv()    # Reload reservations
    formatted_reservations = []
    for r in reservations:
        formatted_reservations.append({
            "table_id": r.get("table_id"),
            "date": r.get("date"),
            "time_start": r.get("time_start"),
            "time_end": r.get("time_end"),
            "party_size": r.get("party_size"),
            "name": r.get("name"),
            "dishes": r.get("dishes", "Not specified"),
            "created_at": r.get("created_at")
        })
    return {
        "total_reservations": len(formatted_reservations),
        "reservations": formatted_reservations
    }


@app.get("/tables")
async def get_tables():
    """Return each table with its reservations, clearly showing table+date+time"""
    reload_business_info()
    load_reservations_from_csv()
    restaurant_info = get_restaurant_info()

    table_map = {t["id"]: {"table_id": t["id"], "capacity": t["capacity"],
                            "name": t["name"], "reservations": []} for t in restaurant_info["tables"]}

    for r in sorted(reservations, key=lambda x: (x["date"], x["time_start"])):
        tid = int(r["table_id"])
        if tid in table_map:
            table_map[tid]["reservations"].append({
                "date":       r["date"],
                "time_start": r["time_start"],
                "time_end":   r["time_end"],
                "party_size": r["party_size"],
                "name":       r["name"],
            })

    return {
        "tables": list(table_map.values()),
        "total_reservations": len(reservations),
    }


@app.get("/")
async def root():
    """Health check"""
    return {"status": "Restaurant AI Assistant API running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
