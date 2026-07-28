"""
Vercel Python Serverless entry point.
"""
import sys
import os

_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app as restaurant_app
from mangum import Mangum


class VercelPathFixer:
    """
    Vercel rewrites /api/chat -> /api/index.py?path=chat.
    This middleware reconstructs the real path from:
      - the 'path' query parameter  (Vercel rewrite style)
      - OR strips /api prefix       (direct invocation style)
    so FastAPI can match its routes correctly.
    """
    def __init__(self, application):
        self.app = application

    async def __call__(self, scope, receive, send):
        if scope.get("type") in ("http", "websocket"):
            path = scope.get("path", "/")
            qs = scope.get("query_string", b"").decode("utf-8", errors="ignore")

            new_path = None
            leftover = []

            # Case 1: Vercel passes original path as ?path=xxx query param
            for part in (qs.split("&") if qs else []):
                if part.startswith("path="):
                    new_path = "/" + part[5:]
                else:
                    leftover.append(part)

            # Case 2: full path like /api/chat received directly
            if new_path is None and path.startswith("/api"):
                new_path = path[4:] or "/"

            if new_path:
                new_qs = "&".join(leftover).encode("utf-8")
                scope = {**scope,
                         "path": new_path,
                         "raw_path": new_path.encode("utf-8"),
                         "query_string": new_qs}

        await self.app(scope, receive, send)


handler = Mangum(VercelPathFixer(restaurant_app), lifespan="off")
