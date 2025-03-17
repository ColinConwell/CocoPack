#!/bin/bash
#
# Shell script wrapper for test_installation.py
# This script provides a simpler interface for running the installation tests

set -e  # Exit immediately if a command exits with a non-zero status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &>/dev/null && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Process command line arguments
KEEP_ENV=false
KEEP_DIST=false
SKIP_BUILD=false
VERBOSE=false

function print_usage() {
  echo "Usage: $0 [options]"
  echo ""
  echo "Options:"
  echo "  -h, --help      Show this help message"
  echo "  -k, --keep-env  Keep test environments after testing"
  echo "  -d, --keep-dist Keep distribution files (wheels, tarballs) after testing"
  echo "  -s, --skip-build Skip build step and use existing wheel/sdist files"
  echo "  -v, --verbose   Show additional output"
  echo ""
}

# Parse command-line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -h|--help)
      print_usage
      exit 0
      ;;
    -k|--keep-env)
      KEEP_ENV=true
      shift
      ;;
    -d|--keep-dist)
      KEEP_DIST=true
      shift
      ;;
    -s|--skip-build)
      SKIP_BUILD=true
      shift
      ;;
    -v|--verbose)
      VERBOSE=true
      shift
      ;;
    *)
      echo "Error: Unknown option: $1"
      print_usage
      exit 1
      ;;
  esac
done

# Build command line arguments
ARGS=""
if [ "$KEEP_ENV" = true ]; then
  ARGS="$ARGS --keep-env"
fi
if [ "$KEEP_DIST" = true ]; then
  ARGS="$ARGS --keep-dist"
fi
if [ "$SKIP_BUILD" = true ]; then
  ARGS="$ARGS --skip-build"
fi
if [ "$VERBOSE" = true ]; then
  ARGS="$ARGS --verbose"
fi

# Ensure the test script is executable
chmod +x "$SCRIPT_DIR/test_installation.py"

# Run the Python test script
echo "Running CocoPack installation tests..."
"$SCRIPT_DIR/test_installation.py" $ARGS

# Exit with the same exit code as the Python script
exit $?