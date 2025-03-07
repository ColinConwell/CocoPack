#!/bin/bash
#
# Test PyPI build workflow locally to verify package structure before publishing.
# This script:
# 1. Creates a temporary build environment
# 2. Builds the package using the same commands as the GitHub workflow
# 3. Installs the built package in a temporary environment
# 4. Runs basic import tests to ensure the package is installable and importable

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail

# Get the repository root directory
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

echo "=== Testing PyPI build from directory: $REPO_ROOT ==="

# Create temporary directories
BUILD_DIR=$(mktemp -d)
INSTALL_DIR=$(mktemp -d)

# Clean up function to remove temporary directories
cleanup() {
  echo "Cleaning up temporary directories..."
  rm -rf "$BUILD_DIR" "$INSTALL_DIR"
}

# Register cleanup function to be called on exit
trap cleanup EXIT

echo "Using build directory: $BUILD_DIR"
echo "Using install directory: $INSTALL_DIR"

# Clean any existing dist directory
rm -rf dist/

# Create virtual environments
echo "Creating build environment..."
python -m venv "$BUILD_DIR/venv"
BUILD_PYTHON="$BUILD_DIR/venv/bin/python"

echo "Creating installation test environment..."
python -m venv "$INSTALL_DIR/venv"
INSTALL_PYTHON="$INSTALL_DIR/venv/bin/python"

# Install build dependencies
echo "Installing build dependencies..."
"$BUILD_PYTHON" -m pip install --upgrade pip build

# Build the package - this simulates what happens in the GitHub workflow
echo "Building package..."
"$BUILD_PYTHON" -m build

# Check that the dist directory now contains wheel and sdist files
if [ ! -d dist ] || [ -z "$(ls -A dist/*.whl 2>/dev/null)" ] || [ -z "$(ls -A dist/*.tar.gz 2>/dev/null)" ]; then
  echo "ERROR: Build did not produce expected files in dist/"
  exit 1
fi

echo "=== Build successful! ==="

# Get the wheel file
WHEEL_FILE=$(ls dist/*.whl | head -n 1)

# Install the built package in the test environment
echo "Installing built package for testing..."
"$INSTALL_PYTHON" -m pip install "$WHEEL_FILE"

# Write a simple test script to verify imports work
TEST_SCRIPT="$INSTALL_DIR/test_import.py"
cat > "$TEST_SCRIPT" << 'EOF'
import sys
print(f"Python version: {sys.version}")
print("Attempting to import cocopack...")
import cocopack
print(f"Successfully imported cocopack (version {cocopack.__version__})")
try:
    import cocopack.notebook
    print("Successfully imported cocopack.notebook")
except ImportError as e:
    print(f"Error importing cocopack.notebook: {e}")
    sys.exit(1)
try:
    import cocopack.shellpack
    print("Successfully imported cocopack.shellpack")
except ImportError as e:
    print(f"Error importing cocopack.shellpack: {e}")
    sys.exit(1)
print("All imports successful!")
EOF

# Run the test script
echo "Testing package imports..."
"$INSTALL_PYTHON" "$TEST_SCRIPT"

echo ""
echo "=== All tests passed! ==="
echo "The package builds successfully and can be imported correctly."
echo "Built files available in $REPO_ROOT/dist"