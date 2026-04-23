#!/usr/bin/env python3
"""
Simple HTTP server to serve the Human Digital Twin frontend.
Run this alongside the FastAPI backend to test the full application.

Usage:
  python serve_frontend.py
  
Then open http://localhost:3000 in your browser.
"""

import http.server
import socketserver
import os
from pathlib import Path

PORT = 3000
FRONTEND_DIR = Path(__file__).parent / "frontend"

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Change to frontend directory
        super().__init__(*args, directory=str(FRONTEND_DIR), **kwargs)

    def log_message(self, format, *args):
        """Log HTTP requests."""
        print(f"[{self.log_date_time_string()}] {format % args}")

def run_server():
    """Start the HTTP server."""
    try:
        with socketserver.TCPServer(("", PORT), MyHttpRequestHandler) as httpd:
            print(f"Starting HTTP server on http://127.0.0.1:{PORT}")
            print(f"Serving files from: {FRONTEND_DIR}")
            print(f"\n>>> Open http://localhost:{PORT} in your browser")
            print(f">>> Make sure backend_api is running: uvicorn backend_api:app --reload")
            print(f"\nPress Ctrl+C to stop the server...\n")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    if not FRONTEND_DIR.exists():
        print(f"ERROR: Frontend directory not found: {FRONTEND_DIR}")
        exit(1)
    
    run_server()
