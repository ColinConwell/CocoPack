.. _shell_api:

=========
Shell API
=========

This section provides detailed documentation for the shell scripts and commands in Coco-Pack.

Command Line Interface
=====================

The Coco-Pack shell utilities can be accessed through the main ``cocopack`` command:

.. code-block:: bash

    cocopack [command] [arguments]

Available Commands
=================

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
===============

colorcode.sh
-----------

Functions for adding color to terminal output.

ezshell.sh
---------

General shell utilities for everyday tasks.

prompt.sh
--------

Prompt customization utilities.

helpers/jekyll.sh
---------------

Helper functions for Jekyll site management.