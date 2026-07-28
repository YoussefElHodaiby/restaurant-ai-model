"""
Vercel Python Serverless entry point for FastAPI.
Checks Vercel headers for the original path.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class VercelHeaderPathMiddleware:
    """
    Middleware that looks for path in Vercel headers.
    Vercel might pass the original path in headers like x-forwarded-path.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            headers = {k.decode('utf-8', errors='ignore').lower(): v.decode('utf-8', errors='ignore') 
                      for k, v in scope.get("headers", [])}
            
            # Log what we receive
            print(f"[VERCEL] PATH: {path}", flush=True)
            print(f"[VERCEL] Query: {scope.get('query_string', b'').decode('utf-8', errors='ignore')}", flush=True)
            
            # Check for Vercel headers
            for header_name in ["x-forwarded-path", "x-original-path", "x-forwarded-uri"]:
                if header_name in headers:
                    print(f"[VERCEL] Found {header_name}: {headers[header_name]}", flush=True)
            
            # Also print all headers that might be useful
            print(f"[VERCEL] All headers: {list(headers.keys())}", flush=True)
        
        await self.app(scope, receive, send)


# Wrap the FastAPI app with our middleware before passing to Mangum
handler = Mangum(VercelHeaderPathMiddleware(app), lifespan="off")
