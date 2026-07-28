# API Documentation

Complete API reference for the Restaurant AI Assistant backend.

## Base URL

```
http://localhost:8000
```

## Authentication

No authentication required (demo project).

## Endpoints

### 1. Health Check

**Endpoint:** `GET /`

**Description:** Check if the API is running.

**Response:**
```json
{
  "status": "Restaurant AI Assistant API running"
}
```

**Status Code:** `200 OK`

---

### 2. Chat

**Endpoint:** `POST /chat`

**Description:** Send a message to the restaurant AI assistant and get a response.

**Request Body:**
```json
{
  "message": "I need a table for 4 tomorrow at 7 PM"
}
```

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| message | string | Yes | User's message to the assistant |

**Response:**
```json
{
  "reply": "I'd be happy to help! Let me check our availability for 4 people tomorrow at 7 PM. We have Table 3 (capacity 4) available. Would you like me to confirm this reservation?"
}
```

**Status Codes:**
| Code | Description |
|------|-------------|
| 200 | Successfully processed message |
| 422 | Invalid request body |
| 500 | Server error |

**Error Response:**
```json
{
  "reply": "Error: DEEPSEEK_API_KEY not configured. Please set it in .env file."
}
```

**Example cURL:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a table for 4 people"}'
```

**Example JavaScript/Fetch:**
```javascript
const response = await fetch('http://localhost:8000/chat', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'I need a table for 4 people'
  })
});

const data = await response.json();
console.log(data.reply);
```

**Example Python/Requests:**
```python
import requests

response = requests.post('http://localhost:8000/chat', json={
    'message': 'I need a table for 4 people'
})

print(response.json()['reply'])
```

**Example Axios:**
```javascript
import axios from 'axios';

const response = await axios.post('http://localhost:8000/chat', {
  message: 'I need a table for 4 people'
});

console.log(response.data.reply);
```

---

### 3. Get Reservations

**Endpoint:** `GET /reservations`

**Description:** Get all current reservations (for debugging/testing).

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

**Status Code:** `200 OK`

**Example cURL:**
```bash
curl http://localhost:8000/reservations
```

**Example JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/reservations');
const data = await response.json();
console.log(data.reservations);
```

---

## Request/Response Models

### ChatMessage (Request)

```python
{
  "message": str  # User's message (required)
}
```

**Validation:**
- `message` must not be empty
- `message` must be a string

### ChatResponse (Response)

```python
{
  "reply": str  # Assistant's response
}
```

---

## Restaurant Information

The assistant has access to this restaurant information:

```python
{
  "name": "AI Restaurant",
  "hours": "11 AM - 10 PM",
  "tables": [
    {"id": 1, "capacity": 2},
    {"id": 2, "capacity": 2},
    {"id": 3, "capacity": 4},
    {"id": 4, "capacity": 4},
    {"id": 5, "capacity": 6}
  ],
  "max_duration_hours": 2
}
```

---

## Reservation Rules

The AI assistant enforces these rules:

1. **Business Hours**: Only 11 AM - 10 PM
2. **Max Duration**: 2 hours per reservation
3. **Party Size**: Must match available table capacity
4. **No Overbooking**: Tables cannot be double-booked
5. **Politeness**: Always respond courteously

---

## Example Conversations

### Example 1: Valid Reservation

**Request:**
```json
{
  "message": "I need a table for 2 people tomorrow at 8 PM"
}
```

**Response:**
```json
{
  "reply": "I'd be happy to help! For 2 people, I can offer you Table 1 or Table 2, both seating 2 people. Tomorrow at 8 PM works perfectly within our hours (11 AM - 10 PM). Would you like me to confirm this reservation?"
}
```

### Example 2: Outside Business Hours

**Request:**
```json
{
  "message": "Can we get a table at 11 PM?"
}
```

**Response:**
```json
{
  "reply": "I'm sorry, but our restaurant closes at 10 PM. We're open from 11 AM to 10 PM. Would you like to book a table earlier in the evening? I'd be happy to find you a spot between 11 AM and 10 PM."
}
```

### Example 3: Party Too Large

**Request:**
```json
{
  "message": "I need a table for 10 people"
}
```

**Response:**
```json
{
  "reply": "I appreciate your interest, but our largest table seats 6 people. We'd love to accommodate your group! Would you be able to split into two groups, or would a table for 6 work for your party? We can also offer two tables to seat everyone together."
}
```

---

## Error Handling

### Missing Environment Variable

**Response:**
```json
{
  "reply": "Error: DEEPSEEK_API_KEY not configured. Please set it in .env file."
}
```

### API Timeout

**Response:**
```json
{
  "reply": "Request to AI service timed out. Please try again."
}
```

### Connection Error

**Response:**
```json
{
  "reply": "Error communicating with AI service: [error details]"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented (demo project). In production, consider:
- Requests per second per IP
- Requests per user per minute
- Request queue management

---

## CORS Configuration

The API accepts requests from:
- `http://localhost:5173` (Frontend dev server)
- `http://localhost:3000` (Alternative dev server)

To add more origins, modify `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://your-domain.com"],
    # ...
)
```

---

## Performance Considerations

- **Timeout**: 30 seconds per request
- **Max Tokens**: 500 tokens per response
- **Temperature**: 0.7 (balanced creativity)
- **In-Memory Storage**: Reservations stored in memory only

---

## Testing Endpoints

### Using Postman

1. Import the collection
2. Set base URL: `http://localhost:8000`
3. Create new POST request to `/chat`
4. Set body to JSON:
   ```json
   {
     "message": "I need a table for 4"
   }
   ```
5. Send request

### Using cURL

```bash
# Chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "I need a table for 4"}'

# Reservations endpoint
curl http://localhost:8000/reservations

# Health check
curl http://localhost:8000/
```

### Using HTTPie

```bash
# Chat endpoint
http POST localhost:8000/chat message="I need a table for 4"

# Reservations
http localhost:8000/reservations

# Health check
http localhost:8000/
```

---

## Troubleshooting

### "DEEPSEEK_API_KEY not configured"
- Create `.env` file in root directory
- Add: `DEEPSEEK_API_KEY=your_key_here`
- Restart backend

### "Connection refused"
- Ensure backend is running: `python backend/main.py`
- Check port 8000 is available
- Try: `lsof -i :8000` to see what's using the port

### "Message not being processed"
- Check frontend is sending correct JSON format
- Verify DEEPSEEK_API_KEY is valid
- Check browser console for errors

### Slow responses
- DeepSeek API might be slow
- Check internet connection
- Try again after a few seconds

---

## API Versioning

Current version: **v1.0.0**

Future versions may introduce:
- `/v2/chat` endpoint with enhanced features
- Authentication tokens
- Rate limiting
- Pagination for reservations

---

## WebSocket Support (Future)

Planned for future versions:
- Real-time chat streaming
- Live table availability updates
- Server-sent events

---

## Related Documentation

- [Backend Code](backend/main.py)
- [Frontend Code](frontend/src/App.jsx)
- [DeepEval Testing Guide](DEEPEVAL_GUIDE.md)
- [Contributing Guide](CONTRIBUTING.md)

---

## Support

For issues or questions:
1. Check [README.md](README.md)
2. Review [DEEPEVAL_GUIDE.md](DEEPEVAL_GUIDE.md)
3. Open a GitHub issue
4. Check existing issues for similar problems

---

**API Documentation v1.0.0** | Last Updated: 2024-01-15
