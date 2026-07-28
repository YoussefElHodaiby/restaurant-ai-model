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
    ASGI middleware that extracts the real path from Vercel's ?path= query param.
    Vercel rewrites /api/chat -> /api/index.py?path=chat
    We need to use /chat as the path so FastAPI routes correctly.
    """
    def __init__(self, application):
        self.app = application

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Debug: log what we receive
            print(f"DEBUG: path={scope.get('path')}, method={scope.get('method')}")
            print(f"DEBUG: query_string={scope.get('query_string')}")
            print(f"DEBUG: raw_path={scope.get('raw_path')}")
            
            # Parse query string to extract ?path=
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")
            parsed = parse_qs(qs)
            print(f"DEBUG: parsed qs={parsed}")
            
            if "path" in parsed:
                # Vercel passed the real path as ?path=chat
                real_path = "/" + parsed["path"][0]
                print(f"DEBUG: extracted real_path={real_path}")
                scope = {
                    **scope,
                    "path": real_path,
                    "raw_path": real_path.encode("utf-8"),
                }
        
        await self.app(scope, receive, send)


handler = Mangum(PathParamMiddleware(app), lifespan="off")
