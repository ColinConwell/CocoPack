import os
import sys
from pathlib import Path
from .cli import get_script_path, source_shell_script

def run_shell_function(script_name, function_name, *args):
    """Run a shell function from a script"""
    script_path = get_script_path(script_name)
    cmd = f"source {script_path} && {function_name} {' '.join(args)}"
    return os.system(cmd)

def path_cleanup_cmd():
    """Direct command for path_cleanup"""
    return run_shell_function('ezshell.sh', 'path_cleanup', *sys.argv[1:])

def color_wrap_cmd():
    """Direct command for color_wrap"""
    return run_shell_function('colorcode.sh', 'color_wrap', *sys.argv[1:])

def jekyll_restart_cmd():
    """Direct command for jekyll_restart"""
    return run_shell_function('helpers/jekyll.sh', 'jekyll_restart', *sys.argv[1:])

def jekyll_reload_cmd():
    """Direct command for jekyll_reload"""
    return run_shell_function('helpers/jekyll.sh', 'jekyll_reload', *sys.argv[1:])

def jekyll_restart_plus_cmd():
    """Direct command for jekyll_restart_plus"""
    return run_shell_function('helpers/jekyll.sh', 'jekyll_restart_plus', *sys.argv[1:])

def clear_git_history_cmd():
    """Direct command for clear_git_history"""
    if len(sys.argv) < 2:
        print("Usage: clear-git-history <commit_message>")
        sys.exit(1)
    script_path = get_script_path('scripts/clear_git_history.sh')
    return run_shell_function(script_path, *sys.argv[1:]) 