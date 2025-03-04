.. _quickstart:

==========
Quickstart
==========

This guide will help you get up and running with Coco-Pack quickly.

Python
======

Jupyter Notebook Styling
-----------------------

One of the most useful features is the Jupyter notebook styling and magic commands:

.. code-block:: python

    from cocopack.notebook import stylizer, magics
    
    # Apply IDE-specific styling
    stylizer.auto_style()
    
    # Enable auto-reload for development
    magics.set_autoreload('complete')

PowerPoint and Keynote
----------------------

Convert presentations to images and PDFs:

.. code-block:: python

    from cocopack.keynote import keynote_to_images, crop_whitespace, convert_to_pdf
    
    # Convert Keynote presentation to PNG images
    keynote_to_images('presentation.key', 'output_folder')
    
    # Crop whitespace around images
    crop_whitespace('output_folder')
    
    # Convert to high-quality PDFs
    convert_all_images_to_pdf('output_folder')

For PowerPoint:

.. code-block:: python

    from cocopack.powerpoint import powerpoint_to_images, crop_whitespace, convert_to_pdf
    
    # Convert PowerPoint presentation to PNG images
    powerpoint_to_images('presentation.pptx', 'output_folder')
    
    # Crop whitespace around images
    crop_whitespace('output_folder')
    
    # Convert to high-quality PDFs
    convert_all_images_to_pdf('output_folder')

Shell
=====

Add to Your Shell Configuration
------------------------------

.. code-block:: bash

    # Add to .bashrc or .zshrc
    eval "$(cocopack prompt)"  # Load prompt utilities
    eval "$(cocopack ezshell)"  # Load shell utilities
    
    # Configure custom prompt
    PS1='$(conda_prompt green) %F{cyan}%n@%m%f $(custom_path) %# '

Path Management
--------------

Clean up your PATH environment variable:

.. code-block:: bash

    path_cleanup --remove-duplicates --remove-empties --apply

Colorize Output
--------------

Add color to your terminal output:

.. code-block:: bash

    color-wrap RED "This text will be red!"
    color-wrap BLUE "This text will be blue!"

R Package
========

Load the Package
---------------

.. code-block:: R

    library(cocopack)
    
    # Or if installed directly from GitHub
    if (!require(pacman)) {install.packages("pacman")}
    pacman::p_load_gh("colinconwell/Coco-Pack-R")

Use Common Functions
------------------

.. code-block:: R

    # Example functions from the R package
    glimpse_data(mtcars)
    
    # More examples to be added as the package develops