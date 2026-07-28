"""
Vercel Python Serverless entry point.
Debug logging to understand what Vercel sends to Mangum.
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
    """Log all request details to understand Vercel's behavior."""
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # Log everything we receive
            print(f"\n{'='*80}")
            print(f"VERCEL REQUEST DEBUG")
            print(f"{'='*80}")
            print(f"PATH: {scope.get('path')}")
            print(f"RAW_PATH: {scope.get('raw_path')}")
            print(f"QUERY_STRING: {scope.get('query_string')}")
            print(f"METHOD: {scope.get('method')}")
            
            # Log all headers
            headers_dict = {}
            for header_name, header_value in scope.get('headers', []):
                headers_dict[header_name.decode('utf-8', errors='ignore')] = header_value.decode('utf-8', errors='ignore')
            print(f"HEADERS:")
            for k, v in headers_dict.items():
                print(f"  {k}: {v}")
            
            print(f"SERVER: {scope.get('server')}")
            print(f"CLIENT: {scope.get('client')}")
            print(f"{'='*80}\n")
        
        await self.app(scope, receive, send)


handler = Mangum(DebugMiddleware(app), lifespan="off")
