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
    """Strip /api prefix from incoming requests."""
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            print(f"[REQUEST] path={path}", file=sys.stderr)
            
            # Strip /api prefix if present
            if path.startswith("/api/"):
                new_path = path[4:]  # Remove "/api"
                print(f"[STRIPPED] {path} -> {new_path}", file=sys.stderr)
                scope = {
                    **scope,
                    "path": new_path,
                    "raw_path": new_path.encode()
                }
            elif path == "/api":
                new_path = "/"
                print(f"[STRIPPED] /api -> /", file=sys.stderr)
                scope = {
                    **scope,
                    "path": new_path,
                    "raw_path": new_path.encode()
                }
        
        await self.app(scope, receive, send)

# Wrap with middleware and Mangum
handler = Mangum(StripApiPrefixMiddleware(app), lifespan="off")
