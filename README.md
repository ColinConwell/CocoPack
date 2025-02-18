# Coco-Pack <img src="logo.png" align="right" width="224px" height="224px" />

Programmatic toolkits for Python, R, and shell scripting. Coco-Pack provides a unified collection of utilities to streamline your development workflow across multiple languages.

*Caveat Emptor*: The core functionality of this codebase is (largely) human-built and human-tested. However, much of the documentation and supporting infrastructure (e.g. installation instructions) has been generated with the help of generative AI. Please use with caution.

Functionality Status:
- [x] Python
- [ ] Shell
- [x] R Package

(Shell commands through the CLI are currently out-of-order, but still work when sourced directly.)

## Quick-Start

### Python Package

```bash
pip install coco-pack
```

### R Package

```R
if (!require(pacman)) {install.packages("pacman")}
pacman::p_load_gh("colinconwell/Coco-Pack-R")
```

### Shell Commands

```bash
pip install "coco-pack[shell]"
```

### Python + Shell

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

**Standalone Package**:

The standalone version of the `coco-pack` R package is available at [Coco-Pack-R](https://colinconwell.github.io/Coco-Pack-R/).

You can install this package by running the following command:

```R
if (!require(pacman)) {install.packages("pacman")}
pacman::p_load_gh("colinconwell/Coco-Pack-R")
```

**Direct Source**:

To directly source the R code from cocopack, you can run the following command:

```R
if (!require(pacman)) {install.packages("pacman")}
pacman::p_load('devtools', 'glue')

repo_url <- 'https://raw.githubusercontent.com/ColinConwell/Coco-Pack/refs/heads/main'
remotes::source_url(glue('{repo_url}/verse/cocopack.R'))
```

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
