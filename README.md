# Coco-Pack <img src="logo.png" align="right" width="224px" height="224px" />

<p style="text-align: justify;">Programmatic toolkits for Python, R, and shell scripting. Coco-Pack provides a unified collection of utilities to streamline your development workflow across multiple languages.</p>

<p style="text-align: justify;"><i>Caveat Emptor</i>: The core functionality of this codebase is (largely) human-built and human-tested. However, much of the documentation and supporting infrastructure (e.g. installation instructions) has been generated with the help of generative AI. Please use with caution and feel free to contribute to the project if you have any improvements or corrections.</p>

## Quick-Start

### Full Installation (Python + Shell)

Install everything (with direct shell commands):
```bash
pip install "coco-pack[shell]"
```

After installation, shell commands are available directly:
```bash
# Use shell commands directly (default)
path-cleanup --remove-duplicates --apply
color-wrap RED "This text will be red!"

# Or use through the cocopack namespace
cocopack ezshell path_cleanup --remove-duplicates --apply
cocopack colorcode
```

### Namespace-Only Installation

If you prefer to keep all commands under the cocopack namespace:
```bash
pip install "coco-pack[namespaced]"
```

This will only install the `cocopack` command:
```bash
cocopack ezshell path_cleanup --remove-duplicates --apply
cocopack prompt
cocopack colorcode
```

### Python Package Only

Install just the Python utilities:
```bash
pip install coco-pack
```

### Uninstallation

Remove everything:
```bash
pip uninstall coco-pack
```

This will remove both Python and shell components. You should also remove any references to cocopack commands from your .bashrc or .zshrc.

### R Package (Coco-Pack-R)

See [verse/README.md](./verse/README.md) for R package installation instructions.

## Common Workflows

### Development Environment Setup

1. Set up your shell environment:
```bash
# Add to .bashrc or .zshrc
eval "$(cocopack prompt)"  # Load prompt utilities
eval "$(cocopack ezshell)"  # Load shell utilities

# Configure custom prompt
PS1='$(conda_prompt green) %F{cyan}%n@%m%f $(custom_path) %# '
```

2. Configure Jupyter environment:
```python
from cocopack.notebook import stylizer, magics

# Apply IDE-specific styling
stylizer.auto_style()

# Enable auto-reload for development
magics.set_autoreload('complete')
```

### Path Management

```bash
# Clean up PATH environment variable
path_cleanup --remove-duplicates --remove-empties --apply
```
