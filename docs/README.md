# Coco-Pack Documentation

This directory contains the documentation for Coco-Pack, built with Sphinx and the PyData theme.

## Building the Documentation

### Prerequisites

Install the documentation dependencies:

```bash
pip install -e ".[docs]"
```

### Build Commands

```bash
# Build the documentation
cd docs
make html

# Clean the build directory
make clean

# Serve the documentation locally
make serve
```

### Quick Preview

For convenience, we provide two scripts to quickly build, serve, and preview the documentation in your browser:

```bash
# Using the shell script
./scripts/preview_docs.sh

# Using the Python script
./scripts/preview_docs.py
```

These scripts will:
1. Build the documentation
2. Start a local web server
3. Open your browser to view the documentation
4. Keep the server running until you press Ctrl+C

After building, the documentation will be available in the `build/html` directory.

## Documentation Structure

- `source/`: Source files for the documentation
  - `_static/`: Static files (CSS, images)
  - `api/`: API reference documentation
  - `user/`: User guides and tutorials
  - `dev/`: Developer documentation
- `build/`: Generated documentation (not committed to the repository)

## Contributing to Documentation

If you're adding a new feature, please also update the documentation accordingly. See the [Contributing Guide](source/dev/contributing.rst) for more information.