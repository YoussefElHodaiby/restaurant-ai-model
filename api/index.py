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


class ASGIDebugMiddleware:
    """
    Debug middleware to understand what scope Vercel sends.
    Tries multiple strategies to reconstruct the real path.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            original_path = scope["path"]
            original_qs = scope.get("query_string", b"").decode()
            
            # Log what we receive
            print(f"SCOPE DEBUG: path={original_path}, qs={original_qs}", file=sys.stderr, flush=True)
            
            # Try to find the real path from multiple sources
            real_path = original_path
            
            # Strategy 1: Check query string for __path or path parameter
            if "__path=" in original_qs:
                try:
                    real_path = "/" + original_qs.split("__path=")[1].split("&")[0]
                    print(f"FIXED from __path: {real_path}", file=sys.stderr, flush=True)
                except:
                    pass
            
            # If we found a better path, update the scope
            if real_path != original_path:
                scope = {
                    **scope,
                    "path": real_path,
                    "raw_path": real_path.encode(),
                }
        
        await self.app(scope, receive, send)


# Wrap with debug middleware
handler = Mangum(ASGIDebugMiddleware(app))
