.. _quickstart:

==========
Quickstart
==========

This guide will help you get up and running with a few of CocoPack's main features.

Python
======

Jupyter Notebook Styling
------------------------

One of the most useful features is the Jupyter notebook styling and magic commands:

.. code-block:: python

    from cocopack.notebook import stylizer, magics
    
    # Apply IDE-specific styling
    stylizer.auto_style()
    
    # Enable auto-reload for development
    magics.set_autoreload('complete')

Presentations and Figures
-------------------------

Convert presentations to images and PDFs:

.. code-block:: python

    from cocopack.figure_ops import slides_to_images, convert_all_images_to_pdf
    
    # Automatically detect file type and convert to PNG images
    slides_to_images('presentation.pptx', 'output_folder', 
                     filename_format='figure{:02d}.png',
                     crop_images=True, 
                     margin_size='0.5cm')
    
    # Convert to high-quality PDFs
    convert_all_images_to_pdf('output_folder')

For specific presentation types:

.. code-block:: python

    from cocopack.figure_ops import keynote_to_images, powerpoint_to_images, crop_whitespace
    
    # For Keynote presentations
    keynote_to_images('presentation.key', 'output_folder')
    
    # For PowerPoint presentations
    powerpoint_to_images('presentation.pptx', 'output_folder')
    
    # Crop whitespace around images
    crop_whitespace('output_folder', margin_size='1cm')

Shell
=====

Add to Your Shell Configuration
-------------------------------

.. code-block:: bash

    # Add to .bashrc or .zshrc
    eval "$(cocopack prompt)"  # Prompt utilities
    eval "$(cocopack ezshell)"  # Shell utilities
    
    # Configure custom prompt
    PS1='$(conda_prompt green) %F{cyan}%n@%m%f $(custom_path) %# '

Path Management
---------------

Clean up your PATH environment variable:

.. code-block:: bash

    path_cleanup --remove-duplicates --remove-empties --apply

Colorize Output
---------------

Add color to your terminal output:

.. code-block:: bash

    color-wrap RED "This text will be red!"
    color-wrap BLUE "This text will be blue!"

R Package
=========

The `cocopack` R package is available at [CocoPack-R](https://colinconwell.github.io/CocoPack-R/).

You can install this package by running the following command:

Load the Package
----------------

.. code-block:: R
    
    if (!require(pacman)) {install.packages("pacman")}
    pacman::p_load_gh("colinconwell/Coco-Pack-R")

Cocopack-R convenience functions include:

.. code-block:: R

    cocopack_r::get_data("iris")
    cocopack_r::plot_histogram("iris$Sepal.Length")
    cocopack_r::fit_lm("iris$Sepal.Length ~ iris$Sepal.Width")