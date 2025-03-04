#!/usr/bin/env python3
"""
Preview Docs - Build and serve Sphinx documentation with auto-browser launch

This script:
1. Builds the Sphinx documentation
2. Launches a local web server
3. Opens a browser to preview the documentation
4. Handles keyboard interrupts gracefully
"""

import os
import sys
import subprocess
import webbrowser
import time
import http.server
import socketserver
import threading
from pathlib import Path

# Define paths relative to the project root
PROJECT_ROOT = Path(__file__).parent.parent.absolute()
DOCS_DIR = PROJECT_ROOT / "docs"
BUILD_DIR = DOCS_DIR / "build" / "html"

def build_docs():
    """Build the documentation using Sphinx"""
    print("Building documentation...")
    os.chdir(DOCS_DIR)
    
    try:
        # Try using make first (better for Unix systems)
        result = subprocess.run(["make", "html"], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE,
                              text=True)
        if result.returncode != 0:
            print("Make failed, trying direct sphinx-build...")
            # Fallback to direct sphinx-build
            result = subprocess.run(
                ["sphinx-build", "-b", "html", "source", "build/html"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
    except FileNotFoundError:
        # If make is not found, try direct sphinx-build
        result = subprocess.run(
            ["sphinx-build", "-b", "html", "source", "build/html"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
    
    if result.returncode != 0:
        print("Error building documentation:")
        print(result.stderr)
        return False
    
    print("Documentation built successfully.")
    return True

def serve_docs(port=8000):
    """Start a simple HTTP server to serve the documentation"""
    os.chdir(BUILD_DIR)
    
    class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            # Suppress log messages
            pass
    
    handler = QuietHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), handler)
    
    print(f"Serving documentation at http://localhost:{port}/")
    print("Press Ctrl+C to stop the server.")
    
    # Create a separate thread for the server
    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True  # This ensures the thread will exit when the main program exits
    server_thread.start()
    
    return httpd

def open_browser(port=8000):
    """Open a web browser to view the documentation"""
    url = f"http://localhost:{port}/"
    print(f"Opening {url} in your browser...")
    webbrowser.open(url)

def main():
    """Main function to build and preview documentation"""
    # Ensure the build directory exists
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    
    # Build the documentation
    if not build_docs():
        sys.exit(1)
    
    # Choose a port
    port = 8000
    
    # Start the server
    httpd = serve_docs(port)
    
    # Give the server a moment to start
    time.sleep(0.5)
    
    # Open the browser
    open_browser(port)
    
    try:
        # Keep the script running until interrupted
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.shutdown()
        print("Server stopped. Goodbye!")

if __name__ == "__main__":
    main()