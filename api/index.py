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


class PathFixMiddleware:
    """
    Fixes path routing for Vercel serverless.
    Vercel rewrites /api/chat to /api/index.py but we need to extract
    the real path from headers or query params.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            original_path = scope["path"]
            
            # Try multiple strategies to find the real path
            real_path = None
            
            # Strategy 1: Check X-Forwarded-Path header
            headers = dict(scope.get("headers", []))
            if b"x-forwarded-path" in headers:
                real_path = headers[b"x-forwarded-path"].decode()
                print(f"Found X-Forwarded-Path: {real_path}", flush=True)
            
            # Strategy 2: Check query string for __path or path param
            if not real_path:
                qs = scope.get("query_string", b"").decode()
                if "__path=" in qs:
                    real_path = "/" + qs.split("__path=")[1].split("&")[0]
                    print(f"Found __path in query: {real_path}", flush=True)
                elif "path=" in qs:
                    real_path = "/" + qs.split("path=")[1].split("&")[0]
                    print(f"Found path in query: {real_path}", flush=True)
            
            # If we found a real path, update the scope
            if real_path and real_path != original_path:
                print(f"Routing from {original_path} to {real_path}", flush=True)
                scope = {
                    **scope,
                    "path": real_path,
                    "raw_path": real_path.encode(),
                }
            else:
                print(f"No path override found, using: {original_path}", flush=True)
        
        await self.app(scope, receive, send)


# Wrap with path fixing middleware
handler = Mangum(PathFixMiddleware(app))
