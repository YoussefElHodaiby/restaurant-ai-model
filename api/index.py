"""
Vercel Python Serverless entry point.
Strips /api prefix from paths before FastAPI routing.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class StripApiPrefixMiddleware:
    """Strip /api/ prefix from the path so FastAPI routes work."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            print(f"DEBUG: Received path: {path}")
            
            if path.startswith("/api/"):
                # Strip /api prefix
                new_path = path[4:]  # Remove "/api"
                print(f"DEBUG: Stripped to: {new_path}")
                scope = {
                    **scope,
                    "path": new_path,
                    "raw_path": new_path.encode("utf-8"),
                }
        
        await self.app(scope, receive, send)


handler = Mangum(StripApiPrefixMiddleware(app), lifespan="off")
