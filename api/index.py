"""
Vercel Python Serverless entry point for FastAPI.
Uses Mangum ASGI adapter to convert FastAPI to AWS Lambda handler.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

# Use Mangum to wrap FastAPI for AWS Lambda/Vercel
# The root_path parameter handles the /api prefix that Vercel adds
handler = Mangum(app, root_path="/api")
