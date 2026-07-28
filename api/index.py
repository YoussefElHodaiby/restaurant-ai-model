"""
Vercel Python Serverless entry point for FastAPI.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

# Simple Mangum wrap - no middleware, no root_path
handler = Mangum(app)
