.. _installation:

============
Installation
============

Coco-Pack can be installed in various configurations depending on which components you need.

Python Package
==============

Basic Installation
------------------

To install just the Python utilities:

.. code-block:: bash

    pip install cocopack

This includes all the core Python functionality without any shell scripts.

Optional Shell CLI
------------------

To install Python utilities along with shell script commands:

.. code-block:: bash

    pip install "cocopack[shell]"

This **Full Installation** provides three ways to access functionality:

- The cocopack namespace command (e.g., ``cocopack colorcode RED "text"``)
- Direct shell script wrappers (e.g., ``cocopack-colorcode RED "text"``)
- Direct Python function wrappers (e.g., ``color-wrap RED "text"``)

After installation, shell commands are available directly:

.. code-block:: bash

    # Use shell commands directly
    path-cleanup --remove-duplicates --apply
    color-wrap RED "This text will be red!"

    # Or use through the cocopack namespace
    cocopack ezshell path_cleanup --remove-duplicates --apply
    cocopack colorcode

Namespaced Installation
-----------------------

If you prefer to keep all commands under the cocopack namespace:

.. code-block:: bash

    pip install "cocopack[namespaced]"

This **Namespace-Only Installation** only provides the ``cocopack`` namespace command:

.. code-block:: bash

    cocopack ezshell path_cleanup --remove-duplicates --apply
    cocopack prompt
    cocopack colorcode

Development Installation
------------------------

For development, install with additional tools:

.. code-block:: bash

    pip install "cocopack[dev]"

This includes testing and linting tools like pytest, black, and isort.

R Package
=========

Standalone Package
------------------

The R package is available from GitHub:

.. code-block:: R

    if (!require(pacman)) {install.packages("pacman")}
    pacman::p_load_gh("colinconwell/CocoPack-R")

Direct Source
-------------

To directly source the R code:

.. code-block:: R

    if (!require(pacman)) {install.packages("pacman")}
    pacman::p_load('devtools', 'glue')

    repo_url <- 'https://raw.githubusercontent.com/ColinConwell/Coco-Pack/refs/heads/main'
    remotes::source_url(glue('{repo_url}/verse/cocopack.R'))

Uninstallation
==============

To remove everything:

.. code-block:: bash

    # First, clean up shell script wrappers
    cocopack uninstall-scripts
    
    # Then uninstall the Python package
    pip uninstall cocopack

You should also remove any references to cocopack commands from your ``.bashrc`` or ``.zshrc``.

Note: When you run ``pip uninstall cocopack``, the package will attempt to automatically clean up shell script wrappers, but it's recommended to run the explicit uninstall command first to ensure all wrappers are properly removed.