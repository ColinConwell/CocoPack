Command Line Tools
==================

CocoPack provides several command-line utilities to help with common tasks. These tools are automatically installed when you install the package.

Main Command: ``cocopack``
--------------------------

The main command is ``cocopack``, which provides access to all shell script utilities in the package.

.. code-block:: bash

    cocopack <command> [args...]

Available commands:

* ``colorcode`` - Colorize text in the terminal
* ``ezshell`` - Various shell utilities

Examples:

.. code-block:: bash

    # Show colorized text
    cocopack colorcode RED "This text will be red"

    # Show disk usage for current directory
    cocopack ezshell show_storage

Direct Commands
---------------

For convenience, CocoPack also provides direct command shortcuts for common operations:

Shell Script Wrappers
^^^^^^^^^^^^^^^^^^^^^

These commands are wrappers around shell scripts:

* ``cocopack-colorcode`` - Colorize text (wraps colorcode.sh)
* ``cocopack-ezshell`` - Shell utilities (wraps ezshell.sh)
* ``cocopack-prompt`` - Prompt utilities (wraps prompt.sh)
* ``cocopack-helpers-jekyll`` - Jekyll helpers (wraps helpers/jekyll.sh)
* ``cocopack-scripts-clear_git_history`` - Git history cleanup (wraps scripts/clear_git_history.sh)
* ``cocopack-scripts-install_cocopack`` - Installation helper (wraps scripts/install_cocopack.sh)

Python Function Wrappers
^^^^^^^^^^^^^^^^^^^^^^^^

These commands are direct wrappers for functions in the shell scripts:

* ``color-wrap`` - Colorize text (wraps color_wrap function)
* ``show-symlinks`` - List symlinks in current directory
* ``show-storage`` - Show storage usage
* ``safe-remove`` - Safely remove files
* ``recursive-cd`` - Recursively change to subdirectory
* ``move-with-symlink`` - Move file and create a symlink
* ``split-path`` - Split a path into components
* ``path-cleanup`` - Clean up a path

Installation
------------

All command-line tools are automatically installed when you install CocoPack:

.. code-block:: bash

    pip install cocopack

If you need to manually install the shell script wrappers (in case they're missing), you can run:

.. code-block:: bash

    cocopack-install

Troubleshooting
---------------

If you encounter issues with the shell script wrappers:

1. Make sure the shell scripts are installed correctly by running ``cocopack-install``
2. Check that the scripts have executable permissions
3. Try using the Python function wrappers instead (e.g., ``color-wrap`` instead of ``cocopack-colorcode``)