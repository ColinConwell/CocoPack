.. _convert:

=============
Convert API
=============

The ``convert`` module provides general-purpose image format conversion utilities.

Main Functions
=============

convert_image
------------

.. autofunction:: python.cocopack.convert.convert_image

This function converts an image from one format to another, with options to handle transparency.

Example:

.. code-block:: python

    from cocopack.convert import convert_image
    
    # Convert a PNG image to JPG
    convert_image('image.png', 'jpg')
    
    # Convert a PNG image to PDF, keeping the original
    convert_image('image.png', 'pdf', remove_original=False)

Helper Functions
==============

_make_opaque
-----------

.. autofunction:: python.cocopack.convert._make_opaque

Internal helper function that converts transparent images to opaque by adding a background.