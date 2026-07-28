"""
Vercel Python Serverless entry point for FastAPI.
Extracts the original path from Vercel's ?path= query parameter.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class VercelPathMiddleware:
    """
    Middleware to fix path routing for Vercel.
    Vercel rewrites /api/chat -> /api/index.py?path=chat
    This extracts the real path from the query param.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Check if we have path in query string
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")
            
            if qs and "path=" in qs:
                # Extract the path parameter
                parts = qs.split("path=")
                if len(parts) > 1:
                    # Get the first value of path param (before any & if multiple params)
                    path_value = parts[1].split("&")[0]
                    # Decode URL-encoded characters if needed
                    import urllib.parse
                    path_value = urllib.parse.unquote(path_value)
                    # Construct the real path
                    new_path = "/" + path_value if not path_value.startswith("/") else path_value
                    
                    print(f"[VERCEL] Extracted path from query: {new_path}", flush=True)
                    
                    # Update the ASGI scope with the real path
                    scope = {
                        **scope,
                        "path": new_path,
                        "raw_path": new_path.encode("utf-8")
                    }
        
        await self.app(scope, receive, send)


# Wrap the FastAPI app with our middleware before passing to Mangum
handler = Mangum(VercelPathMiddleware(app), lifespan="off")
