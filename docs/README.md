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