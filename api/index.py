"""
Vercel Python Serverless entry point for FastAPI.
Logs all ASGI scope details to debug Vercel routing.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class DebugPathMiddleware:
    """
    Debug middleware that logs all scope details.
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            path = scope.get("path", "")
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")
            method = scope.get("method", "")
            
            print(f"\n{'='*80}", flush=True)
            print(f"[VERCEL] INCOMING REQUEST", flush=True)
            print(f"[VERCEL] PATH: {path}", flush=True)
            print(f"[VERCEL] QUERY_STRING: {qs}", flush=True)
            print(f"[VERCEL] METHOD: {method}", flush=True)
            print(f"[VERCEL] RAW_PATH: {scope.get('raw_path')}", flush=True)
            
            # Log all headers
            print(f"[VERCEL] HEADERS:", flush=True)
            for name, value in scope.get("headers", []):
                name_str = name.decode("utf-8", errors="ignore")
                value_str = value.decode("utf-8", errors="ignore")
                if name_str.lower() in ["x-forwarded-path", "x-original-path", "x-forwarded-uri"]:
                    print(f"  {name_str}: {value_str}", flush=True)
            
            print(f"{'='*80}\n", flush=True)
            
            # Try to extract real path from query string
            if qs and "path=" in qs:
                try:
                    path_value = qs.split("path=")[1].split("&")[0]
                    import urllib.parse
                    path_value = urllib.parse.unquote(path_value)
                    new_path = "/" + path_value if not path_value.startswith("/") else path_value
                    
                    print(f"[FIX] Changing path from {path} to {new_path}", flush=True)
                    
                    scope = {
                        **scope,
                        "path": new_path,
                        "raw_path": new_path.encode("utf-8")
                    }
                except Exception as e:
                    print(f"[ERROR] Failed to extract path: {e}", flush=True)
        
        await self.app(scope, receive, send)


# Wrap the FastAPI app with our middleware before passing to Mangum
handler = Mangum(DebugPathMiddleware(app), lifespan="off")
