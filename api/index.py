"""
Vercel Python Serverless entry point for FastAPI.
"""
import sys
import os
import json

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum

class DebugMiddleware:
    """Log and fix path routing for Vercel."""
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            method = scope.get("method", "")
            qs = scope.get("query_string", b"").decode("utf-8")
            
            # Log everything to stderr for Vercel function logs
            log_msg = f"[VERCEL] path={path} method={method} qs={qs}"
            print(log_msg, file=sys.stderr, flush=True)
            
            # Try multiple strategies to fix the path
            new_path = path
            
            # Strategy 1: If path starts with /api, strip it
            if path.startswith("/api/"):
                new_path = path[4:]  # Remove "/api"
                print(f"[FIX1] Stripped /api prefix: {path} -> {new_path}", file=sys.stderr, flush=True)
            # Strategy 2: Check if /api in query string
            elif "path=" in qs:
                try:
                    path_value = qs.split("path=")[1].split("&")[0]
                    new_path = "/" + path_value
                    print(f"[FIX2] Extracted path from query: {path_value} -> {new_path}", file=sys.stderr, flush=True)
                except Exception as e:
                    print(f"[FIX2_ERROR] {e}", file=sys.stderr, flush=True)
            # Strategy 3: If path is just /api or empty, default to /
            elif path in ["/api", "/", ""]:
                new_path = "/"
            
            if new_path != path:
                scope = {
                    **scope,
                    "path": new_path,
                    "raw_path": new_path.encode()
                }
                print(f"[SCOPE_UPDATED] {path} -> {new_path}", file=sys.stderr, flush=True)
            else:
                print(f"[NO_CHANGE] path={path}", file=sys.stderr, flush=True)
        
        await self.app(scope, receive, send)

# Wrap with middleware
handler = Mangum(DebugMiddleware(app), lifespan="off")
