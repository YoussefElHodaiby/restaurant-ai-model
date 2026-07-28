"""
Vercel Python Serverless entry point.
Extracts the real path from ?path= query param that Vercel adds.
"""
import sys
import os
from urllib.parse import parse_qs

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class ExtractRealPathMiddleware:
    """
    Vercel rewrites /api/chat to /api/index.py but passes the real path as ?path=chat.
    This middleware extracts the real path from query params and uses it for routing.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Vercel passes the real path as a query param
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")
            print(f"DEBUG: query_string = {qs}")
            
            if qs and "path=" in qs:
                # Parse query string
                parsed = parse_qs(qs)
                if "path" in parsed:
                    real_path = "/" + parsed["path"][0]
                    print(f"DEBUG: Extracted real_path from query param: {real_path}")
                    
                    # Replace the path in the scope
                    scope = {
                        **scope,
                        "path": real_path,
                        "raw_path": real_path.encode("utf-8"),
                        # Keep the query_string for any downstream code that might use it
                    }
            else:
                print(f"DEBUG: No path query param found, using original path: {scope.get('path')}")
        
        await self.app(scope, receive, send)


handler = Mangum(ExtractRealPathMiddleware(app), lifespan="off")
