# Coco-Pack Shell (Coco-ShPack)

Shell utilities for Coco-Pack, available through the `cocopack` command when installed.

## Installation

Shell utilities are installed as part of the full Coco-Pack installation:
```bash
pip install "coco-pack[shell]"
```

## Usage

### Direct Commands (Default)

```bash
# Use shell commands directly
path-cleanup --remove-duplicates --apply
color-wrap RED "This text will be red!"
jekyll-restart 4000
```

### Namespaced Commands

```bash
# Use through cocopack namespace
cocopack ezshell path_cleanup --remove-duplicates --apply
cocopack prompt
cocopack colorcode
```

## Uninstallation

```bash
pip uninstall coco-pack
```

After uninstallation:
1. Remove cocopack-related lines from your .bashrc or .zshrc
2. Clean up any remaining shell scripts: `rm -f ~/.local/bin/cocopack*`
