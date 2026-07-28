"""
Vercel Python Serverless entry point.
Handles path rewriting for FastAPI on Vercel.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

# Wrap FastAPI app with middleware to fix path routing
from fastapi import FastAPI

class PathFixMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope["path"]
            print(f"[PATH] Received path: {path}", file=sys.stderr)
            
            # Check if path is /api/index or similar - if so, check for the real path in query string
            if "/index" in path or path == "/":
                qs = scope.get("query_string", b"").decode("utf-8")
                print(f"[QS] Query string: {qs}", file=sys.stderr)
                
                if "path=" in qs:
                    # Extract path from query param
                    path_value = qs.split("path=")[1].split("&")[0]
                    new_path = "/" + path_value
                    print(f"[FIX] Extracted new path: {new_path}", file=sys.stderr)
                    scope = {
                        **scope,
                        "path": new_path,
                        "raw_path": new_path.encode()
                    }
        
        await self.app(scope, receive, send)

# Use PathFixMiddleware to handle Vercel's path rewriting
handler = Mangum(PathFixMiddleware(app), lifespan="off")
