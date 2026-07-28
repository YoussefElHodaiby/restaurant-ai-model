"""
Vercel Python Serverless entry point.
Handles Vercel's path rewriting via query param.
"""
import sys
import os
from urllib.parse import parse_qs

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class PathParamMiddleware:
    """
    ASGI middleware that extracts the real path from Vercel's rewrite.
    Tries multiple strategies:
    1. Check query param ?path=
    2. Check X-Forwarded-Path header
    3. Check Vercel-provided env vars
    """
    def __init__(self, application):
        self.app = application

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Debug: log what we receive
            print(f"DEBUG: path={scope.get('path')}, method={scope.get('method')}")
            print(f"DEBUG: query_string={scope.get('query_string')}")
            print(f"DEBUG: raw_path={scope.get('raw_path')}")
            print(f"DEBUG: headers={dict(scope.get('headers', []))}")
            
            # Try to extract real path
            real_path = None
            
            # Strategy 1: Check query string for ?path=
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")
            parsed = parse_qs(qs)
            if "path" in parsed:
                real_path = "/" + parsed["path"][0]
                print(f"DEBUG: found path in query string: {real_path}")
            
            # Strategy 2: Check X-Forwarded-Path header
            if not real_path:
                headers = dict(scope.get("headers", []))
                for key, value in headers.items():
                    if key.lower() == b"x-forwarded-path":
                        real_path = value.decode("utf-8", errors="ignore")
                        print(f"DEBUG: found X-Forwarded-Path: {real_path}")
                        break
            
            # Apply the real path if found
            if real_path:
                scope = {
                    **scope,
                    "path": real_path,
                    "raw_path": real_path.encode("utf-8"),
                }
                print(f"DEBUG: modified scope.path to: {real_path}")
        
        await self.app(scope, receive, send)


handler = Mangum(PathParamMiddleware(app), lifespan="off")
