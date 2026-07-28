"""
Vercel Python Serverless entry point for FastAPI.
Sets root_path for FastAPI running under /api/ prefix.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

# For Vercel: FastAPI is running under /api/ prefix, so set root_path
# This tells Mangum/FastAPI to expect requests like /api/chat to work with @app.post("/chat")
handler = Mangum(app, root_path="/api")
