import os, subprocess
from pathlib import Path

def get_script_path(script_name):
    """Get the full path to a shell script"""
    package_dir = Path(__file__).parent.parent.parent.parent
    return package_dir / 'shell' / script_name

def run_shell_script(script_path, *args):
    """Run a shell script with arguments"""
    cmd = ['/bin/bash', str(script_path)] + list(args)
    subprocess.run(cmd, check=True)

def clear_git_history():
    """Python wrapper for clear_git_history.sh"""
    script = get_script_path('scripts/clear_git_history.sh')
    import sys
    if len(sys.argv) < 2:
        print("Usage: clear-git-history <commit_message>")
        sys.exit(1)
    run_shell_script(script, sys.argv[1])

def jekyll_restart():
    """Python wrapper for jekyll_restart"""
    script = get_script_path('helpers/jekyll.sh')
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "4000"
    # Source the script and call the function
    os.system(f"source {script} && jekyll_restart {port}")

def jekyll_reload():
    """Python wrapper for jekyll_reload"""
    script = get_script_path('helpers/jekyll.sh')
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "4000"
    os.system(f"source {script} && jekyll_reload {port}")

def jekyll_restart_plus():
    """Python wrapper for jekyll_restart_plus"""
    script = get_script_path('helpers/jekyll.sh')
    import sys
    port = sys.argv[1] if len(sys.argv) > 1 else "4000"
    os.system(f"source {script} && jekyll_restart_plus {port}") 