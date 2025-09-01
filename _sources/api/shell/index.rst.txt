.. _shell_api:

=========
Shell API
=========

This section provides detailed documentation for the shell scripts and commands in Coco-Pack.

Command Line Interface
======================

The Coco-Pack shell utilities can be accessed through the main ``cocopack`` command:

.. code-block:: bash

    cocopack [command] [arguments]

Available Commands
==================

prompt
------

Shell prompt customization utilities.

.. code-block:: bash

    cocopack prompt

ezshell
-------

Everyday shell utility functions.

.. code-block:: bash

    cocopack ezshell [command] [arguments]

colorcode
---------

Colorize terminal output.

.. code-block:: bash

    cocopack colorcode
    # Or directly
    color-wrap RED "This text will be red!"

Script Reference
================

colorcode.sh
------------

Functions for adding color to terminal output.

**Key Functions:**

* ``color_wrap`` - Wrap text with color codes for terminal output
* ``prompt_color`` - Convert regular color codes to prompt-compatible format (for use in PS1/prompt customization)

Example usage of ``prompt_color`` in a custom bash prompt:

.. code-block:: bash

    # In your .bashrc or .zshrc
    source /path/to/cocopack/colorcode.sh
    
    # For bash PS1 customization
    PS1="$(prompt_color GREEN)\u@\h$(prompt_color RESET):$(prompt_color BLUE)\w$(prompt_color RESET)\\$ "
    
    # For zsh prompt customization
    PROMPT='$(prompt_color GREEN)%n@%m$(prompt_color RESET):$(prompt_color BLUE)%~$(prompt_color RESET)%# '

ezshell.sh
----------

General shell utilities for everyday tasks.

prompt.sh
---------

Prompt customization utilities.

helpers/jekyll.sh
-----------------

Helper functions for Jekyll site management.