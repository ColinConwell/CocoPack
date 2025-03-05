.. _figure_ops:

=================
Figure Operations
=================

The ``figure_ops`` module provides functionality for converting PowerPoint and Keynote presentations to images and PDFs, with options for cropping and reformatting.

Main Functions
==============

slides_to_images
----------------

.. autofunction:: python.cocopack.figure_ops.slides_to_images
    :no-index:

This is the primary function that detects file type (.key, .ppt, .pptx) and applies the appropriate conversion method.

Example:

.. code-block:: python

    from cocopack.figure_ops import slides_to_images
    
    # Convert a presentation to PNG images, cropping whitespace
    slides_to_images('presentation.pptx', 'output_folder', 
                    filename_format='figure{:02d}.png',
                    crop_images=True,
                    margin_size='0.5cm')


Presentation Conversion
=======================

keynote_to_images
-----------------

.. autofunction:: python.cocopack.figure_ops.keynote_to_images
    :no-index:

Example:

.. code-block:: python

    from cocopack.figure_ops import keynote_to_images
    
    # Convert a Keynote presentation to PNG images
    keynote_to_images('presentation.key', 'output_folder')

powerpoint_to_images
--------------------

.. autofunction:: python.cocopack.figure_ops.powerpoint_to_images
    :no-index:

Example:

.. code-block:: python

    from cocopack.figure_ops import powerpoint_to_images
    
    # Convert a PowerPoint presentation to PNG images
    powerpoint_to_images('presentation.pptx', 'output_folder')


Image Processing
================

crop_whitespace
---------------

.. autofunction:: python.cocopack.figure_ops.crop_whitespace
    :no-index:
    
Example:

.. code-block:: python

    from cocopack.figure_ops import crop_whitespace
    
    # Crop whitespace from all images in a folder
    crop_whitespace('output_folder', margin_size='1cm')

PDF Conversion
==============

convert_to_pdf
--------------

.. autofunction:: python.cocopack.figure_ops.convert_to_pdf
    :no-index:

Example:

.. code-block:: python

    from cocopack.figure_ops import convert_to_pdf
    
    # Convert a PNG image to PDF
    convert_to_pdf('image.png', dpi=300)

convert_all_images_to_pdf
-------------------------

.. autofunction:: python.cocopack.figure_ops.convert_all_images_to_pdf
    :no-index:

Example:

.. code-block:: python

    from cocopack.figure_ops import convert_all_images_to_pdf
    
    # Convert all PNG images in a folder to PDFs
    convert_all_images_to_pdf('output_folder', dpi=300)

Platform Support
================

The module provides platform-specific implementations:

* **macOS**: Uses AppleScript to interact with Keynote and PowerPoint alike
* **Windows**: Uses the COM interface (via pywin32) to control PowerPoint
* **Linux/Other**: Uses LibreOffice command-line tools with python-pptx as a fallback