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

class StripApiPrefixMiddleware:
    """Strip /api prefix from paths so FastAPI routes work correctly."""
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            
            # If path starts with /api/, strip it so FastAPI gets the right route
            if path.startswith("/api/"):
                new_path = path[4:]  # Remove "/api" prefix
                scope = {
                    **scope,
                    "path": new_path,
                    "raw_path": new_path.encode()
                }
        
        await self.app(scope, receive, send)

# Wrap FastAPI with middleware and create Mangum handler
handler = Mangum(StripApiPrefixMiddleware(app), lifespan="off")

