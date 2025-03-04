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
script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
project_root="$(dirname "$script_dir")"
docs_dir="$project_root/docs"
build_dir="$docs_dir/build/html"

# Colors for terminal output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to open a browser (cross-platform)
open_browser() {
    local url="$1"
    echo -e "${GREEN}Opening $url in your browser...${NC}"
    
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
        echo -e "${YELLOW}Could not automatically open browser. Please manually open:${NC}"
        echo -e "${YELLOW}$url${NC}"
    fi
}

# Build the documentation
build_docs() {
    echo -e "${GREEN}Building documentation...${NC}"
    cd "$docs_dir" || { echo -e "${RED}Could not change to docs directory${NC}"; exit 1; }
    
    # Try using make first
    if command_exists make; then
        if make html; then
            echo -e "${GREEN}Documentation built successfully.${NC}"
            return 0
        else
            echo -e "${YELLOW}Make failed, trying direct sphinx-build...${NC}"
        fi
    fi
    
    # Fallback to sphinx-build
    if command_exists sphinx-build; then
        if sphinx-build -b html source build/html; then
            echo -e "${GREEN}Documentation built successfully.${NC}"
            return 0
        else
            echo -e "${RED}Failed to build documentation.${NC}"
            return 1
        fi
    else
        echo -e "${RED}Neither make nor sphinx-build commands found. Please install Sphinx.${NC}"
        return 1
    fi
}

# Start a web server
serve_docs() {
    local port="$1"
    cd "$build_dir" || { echo -e "${RED}Could not change to build directory${NC}"; exit 1; }
    
    echo -e "${GREEN}Serving documentation at http://localhost:$port/${NC}"
    echo -e "${YELLOW}Press Ctrl+C to stop the server.${NC}"
    
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
        echo -e "${RED}Could not find Python to start a server.${NC}"
        return 1
    fi
}

# Main function
main() {
    # Make sure the build directory exists
    mkdir -p "$build_dir"
    
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