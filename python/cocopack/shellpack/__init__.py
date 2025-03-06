from . import commands as shell_commands
from .install import install_shell_scripts

__all__ = ['shell_commands', 'install_shell_scripts']

# Automatically attempt to install shell scripts during import
try:
    install_shell_scripts()
except Exception:
    # Silently fail if installation fails, this is just a convenience
    pass
