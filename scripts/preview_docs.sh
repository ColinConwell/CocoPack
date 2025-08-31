#!/usr/bin/env bash
#
# Preview Docs - Build and serve Sphinx documentation with auto-browser launch
# 
# This script:
# 1. Builds the Sphinx documentation
# 2. Launches a local web server
# 3. Opens a browser to preview the documentation
# 4. Handles keyboard interrupts gracefully

set -e

# Determine the project root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
DOCS_DIR="$PROJECT_ROOT/docs"
BUILD_DIR="$DOCS_DIR/_build"
BUILD_DIR_HTML="$BUILD_DIR/html"

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NOCOLOR='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open a browser (cross-platform)
open_browser() {
    local url="$1"
    echo -e "${GREEN}Opening $url in your browser...${NOCOLOR}"
    
    if command_exists open; then
        # macOS
        open "$url"
    elif command_exists xdg-open; then
        # Linux
        xdg-open "$url"
    elif command_exists python3; then
        # Fallback to Python's webbrowser
        python3 -m webbrowser "$url"
    elif command_exists python; then
        # Another fallback
        python -m webbrowser "$url"
    else
        echo -e "${YELLOW}Could not automatically open browser. Please manually open:${NOCOLOR}"
        echo -e "${YELLOW}$url${NOCOLOR}"
    fi
}

# Build the documentation
build_docs() {
    echo -e "${GREEN}Building documentation...${NOCOLOR}"
    cd "$DOCS_DIR" || { echo -e "${RED}Could not change to docs directory${NOCOLOR}"; exit 1; }
    
    # Try using make first
    if command_exists make; then
        if make html; then
            echo -e "${GREEN}Documentation built successfully in $BUILD_DIR_HTML.${NOCOLOR}"
            return 0
        else
            echo -e "${YELLOW}Make failed, trying direct sphinx-build...${NOCOLOR}"
        fi
    fi
    
    # Fallback to sphinx-build
    if command_exists sphinx-build; then
        if sphinx-build -b html source $BUILD_DIR_HTML; then
            echo -e "${GREEN}Documentation built successfully in $BUILD_DIR_HTML.${NOCOLOR}"
            return 0
        else
            echo -e "${RED}Failed to build documentation.${NOCOLOR}"
            return 1
        fi
    else
        echo -e "${RED}Neither make nor sphinx-build commands found. Please install Sphinx.${NOCOLOR}"
        return 1
    fi
}

# Start a web server
serve_docs() {
    local port="$1"
    cd "$BUILD_DIR_HTML" || { echo -e "${RED}Could not change to build directory${NOCOLOR}"; exit 1; }
    
    echo -e "${GREEN}Serving documentation at http://localhost:$port/${NOCOLOR}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server.${NOCOLOR}"
    
    # Try different server methods
    if command_exists python3; then
        python3 -m http.server "$port"
    elif command_exists python; then
        # Check if Python is version 3 or has http.server
        if python -c "import http.server" 2>/dev/null; then
            python -m http.server "$port"
        else
            python -m SimpleHTTPServer "$port"
        fi
    else
        echo -e "${RED}Could not find Python to start a server.${NOCOLOR}"
        return 1
    fi
}

# Main function
main() {
    # Make sure the build directory exists
    mkdir -p "$BUILD_DIR_HTML"
    
    # Build the docs
    build_docs || exit 1
    
    # Choose a port
    local port=8000
    
    # Open the browser in the background
    open_browser "http://localhost:$port/" &
    
    # Small delay to allow the browser to be ready
    sleep 1
    
    # Start the server (this will block until Ctrl+C)
    serve_docs "$port"
}

# Run the main function
main "$@"