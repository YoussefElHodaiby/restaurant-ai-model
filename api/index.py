"""
Vercel Python Serverless entry point.
"""
import sys
import os

# Make backend/ importable and set CWD so CSV files resolve correctly
_backend_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend")
sys.path.insert(0, _backend_dir)
os.chdir(_backend_dir)

from main import app
from mangum import Mangum


class StripApiPrefix:
    """
    ASGI middleware that strips /api prefix from the request path before
    FastAPI sees it.  Vercel forwards the full path (/api/chat) to the
    function, but FastAPI only knows the route /chat.
    """
    def __init__(self, application, prefix: str = "/api"):
        self.app = application
        self.prefix = prefix.encode()
        self.prefix_str = prefix

    async def __call__(self, scope, receive, send):
        if scope.get("type") in ("http", "websocket"):
            path: str = scope.get("path", "")
            if path.startswith(self.prefix_str):
                stripped = path[len(self.prefix_str):] or "/"
                scope = {**scope, "path": stripped}
                raw: bytes = scope.get("raw_path", b"")
                if raw.startswith(self.prefix):
                    scope["raw_path"] = raw[len(self.prefix):] or b"/"
        await self.app(scope, receive, send)


handler = Mangum(StripApiPrefix(app), lifespan="off")
