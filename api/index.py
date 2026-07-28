"""
Vercel Python Serverless entry point.
Uses Mangum to run FastAPI on Vercel's serverless environment.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

# Mangum converts ASGI (FastAPI) to AWS Lambda/Vercel format
# root_path="/api" tells it to strip /api prefix from incoming requests
# so /api/chat becomes /chat for FastAPI routing
handler = Mangum(app, lifespan="off", root_path="/api")
