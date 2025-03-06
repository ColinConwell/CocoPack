"""
Shell script installation utilities.
"""
import os
import sys
import site
import shutil
from pathlib import Path

def get_shell_scripts_dir():
    """Get the directory where shell scripts are stored"""
    # First check if we're in development mode
    package_dir = Path(__file__).parent.parent
    shell_dir = package_dir / 'shell'
    
    if not shell_dir.exists():
        # Try repository root
        repo_root = Path(__file__).parent.parent.parent.parent
        shell_dir = repo_root / 'shell'
    
    return shell_dir if shell_dir.exists() else None

def get_bin_dir():
    """Get the directory where scripts should be installed"""
    # Use the same bin directory where pip installs scripts
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        bin_dir = Path(sys.prefix) / 'bin'
    else:
        # We're in a regular Python installation, use user directory
        bin_dir = Path(sys.prefix) / 'bin'
        
        # For user installs, use user bin directory
        if not os.access(bin_dir, os.W_OK):
            user_base = Path(site.getuserbase()) if hasattr(site, 'getuserbase') else Path.home() / '.local'
            bin_dir = user_base / 'bin'
            bin_dir.mkdir(parents=True, exist_ok=True)
    
    return bin_dir

def create_script_symlink(src_path, bin_dir, script_name):
    """Create a wrapper script for a shell script"""
    dest_path = bin_dir / f"cocopack-{script_name.replace('.sh', '')}"
    
    # Check if script exists
    if dest_path.exists():
        dest_path.unlink()  # Remove existing file or link
    
    # Always create a wrapper script instead of symlink for better compatibility
    with open(dest_path, 'w') as f:
        f.write(f"""#!/bin/bash
# This is an auto-generated wrapper for CocoPack
# Original script: {src_path}

if [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    echo "CocoPack Shell Script: {script_name}"
    echo "Usage: $(basename $0) [arguments]"
    echo ""
    echo "This is a wrapper around {src_path}"
    exit 0
fi

# Source the script for functions
source "{src_path}"

# If the script contains a function with the same name as the file (without .sh)
# execute that function, otherwise just source the script
func_name="{script_name.replace('.sh', '')}"
if declare -f "$func_name" > /dev/null; then
    "$func_name" "$@"
elif declare -f "color_wrap" > /dev/null && [ "{script_name}" = "colorcode.sh" ]; then
    # Special case for colorcode.sh
    if [ $# -lt 2 ]; then
        echo "Usage: $(basename $0) COLOR TEXT"
        echo "  COLOR: color name (e.g., RED, BOLD_BLUE)"
        echo "  TEXT: the text to colorize"
        exit 1
    fi
    color_wrap "$1" "$2"
fi
""")
        os.chmod(dest_path, 0o755)  # Make executable

def install_shell_scripts():
    """Install shell scripts to the bin directory"""
    shell_dir = get_shell_scripts_dir()
    if not shell_dir:
        return  # No shell scripts directory found
    
    bin_dir = get_bin_dir()
    if not bin_dir:
        return  # No bin directory found
    
    # Install main shell scripts
    for script_file in shell_dir.glob('*.sh'):
        create_script_symlink(script_file, bin_dir, script_file.name)
    
    # Install helper scripts
    helpers_dir = shell_dir / 'helpers'
    if helpers_dir.exists():
        for script_file in helpers_dir.glob('*.sh'):
            create_script_symlink(script_file, bin_dir, f"helpers-{script_file.name}")
    
    # Install utility scripts
    scripts_dir = shell_dir / 'scripts'
    if scripts_dir.exists():
        for script_file in scripts_dir.glob('*.sh'):
            create_script_symlink(script_file, bin_dir, f"scripts-{script_file.name}")

if __name__ == "__main__":
    install_shell_scripts()