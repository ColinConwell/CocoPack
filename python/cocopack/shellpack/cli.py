import os, sys, subprocess
from pathlib import Path
from warnings import warn

from .install import uninstall_shell_scripts

SHELL_COMMANDS = {
    'ezshell': 'ezshell.sh',
    'colorcode': 'colorcode.sh',
    'prompt': 'prompt.sh',
}

def get_script_path(script_name):
    """Get the full path to a shell script"""
    # First look in the package directory
    package_dir = Path(__file__).parent.parent
    script_path = package_dir / 'shell' / script_name
    
    if script_path.exists():
        return script_path
    
    # If not found, look in the repository root
    repo_root = Path(__file__).parent.parent.parent.parent
    script_path = repo_root / 'shell' / script_name
    
    if script_path.exists():
        return script_path
    
    # If still not found, look in the installed scripts
    import shutil
    cmd_path = shutil.which(f"cocopack-{script_name.replace('.sh', '')}")
    if cmd_path:
        return Path(cmd_path)
    
    # Return the original path, even though it doesn't exist
    return package_dir / 'shell' / script_name

def run_script(script_path, *args):
    """Run a shell script with arguments"""
    cmd = ['/bin/bash', str(script_path)] + list(args)
    subprocess.run(cmd, check=True)

def print_usage():
    """Print usage information"""
    print("Usage: cocopack <command> [args...]")
    print("\nAvailable commands:")
    for cmd in SHELL_COMMANDS:
        print(f"  {cmd}")
    print("\nSpecial commands:")
    print("  uninstall-scripts - Remove shell script wrappers from bin directory")
    print("\nFor command-specific help:")
    print("  cocopack <command> --help")

def source_shell_script(script_path, *args):
    """Source a shell script and run a command"""
    script_name = Path(script_path).stem  # Get the name without extension
    
    # Handle help flag
    if args and (args[0] == '--help' or args[0] == '-h'):
        print(f"Help for {script_name}:")
        # For colorcode, display specific help
        if script_name == 'colorcode':
            print("Usage: cocopack colorcode COLOR TEXT")
            print("  COLOR: color name from the colorcode.sh script (e.g., RED, BOLD_BLUE)")
            print("  TEXT: the text to colorize")
            return 0
        # For other scripts, just source them and extract help
        cmd = f"source {script_path} && if [ \"$(type -t {script_name}_help)\" = function ]; then {script_name}_help; else echo 'No help available for {script_name}'; fi"
        return os.system(cmd)
    
    # For colorcode, handle the color_wrap function
    if script_name == 'colorcode':
        if len(args) < 2:
            print("Error: colorcode requires COLOR and TEXT arguments")
            print("Use 'cocopack colorcode --help' for more information")
            return 1
        text = ' '.join(args[1:])
        cmd = f"bash -c 'source {script_path} && color_wrap {args[0]} \"{text}\"'"
    else:
        # For other scripts, just source and run any commands
        cmd = f"source {script_path}"
        if args:
            cmd += f" && {' '.join(args)}"
    
    return os.system(cmd)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help']:
        print_usage()
        sys.exit(0)

    command = sys.argv[1]
    
    # Handle special commands
    if command == 'uninstall-scripts':
        print("Uninstalling shell script wrappers...")
        uninstall_shell_scripts()
        print("Done.")
        sys.exit(0)
    
    if command not in SHELL_COMMANDS:
        print(f"Unknown command: {command}")
        print_usage()
        sys.exit(1)

    script_path = get_script_path(SHELL_COMMANDS[command])
    if not script_path.exists():
        print(f"Script not found: {script_path}")
        sys.exit(1)

    # Pass remaining arguments to the script
    args = sys.argv[2:]
    exit_code = source_shell_script(script_path, *args)
    sys.exit(exit_code >> 8)  # Convert shell exit code to Python exit code

if __name__ == '__main__':
    main() 