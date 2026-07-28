"""
Vercel Python Serverless entry point.
Imports the FastAPI app from backend/main.py and wraps it with Mangum
so it runs as an AWS Lambda-style handler (Vercel's Python runtime).
"""
import sys
import os

# Make backend/ importable and set CWD so relative CSV paths resolve correctly
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app  # FastAPI app
from mangum import Mangum

# Mangum bridges ASGI (FastAPI) to Vercel's Lambda runtime.
# api_gateway_base_path strips /api prefix before FastAPI sees the request,
# so routes like /chat, /reservations, /tables all work unchanged.
handler = Mangum(app, lifespan="off", api_gateway_base_path="/api")
