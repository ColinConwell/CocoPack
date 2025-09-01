.. _index:

Welcome to CocoPack's Documentation
===================================

.. image:: ../../logo.png
   :width: 180px
   :align: right
   :alt: CocoPack Logo

CocoPack is a collection of programmatic toolkits for Python, R, and shell scripting. It provides a unified set of utilities to streamline your development workflow across multiple languages.

.. note::

   *Caveat Emptor*: All code in this package has been tested by a human (me), but I've made ample use of a custom generative AI pipeline for (auto-)documentation.

Features
--------

* **Python Utilities**: Tools for data processing, visualization, and automation
* **Shell CLI**: Command-line tools for common tasks and workflows
* **R Package**: Tools for statistics, data manipulation, and visualization

(Note, the R package has now been moved to a standalone package, found [here](https://github.com/ColinConwell/CocoPack-R/).)

Quick Start
-----------

Python Package
^^^^^^^^^^^^^^

.. code-block:: bash

   pip install cocopack

R Package
^^^^^^^^^

.. code-block:: R

   if (!require(pacman)) {install.packages("pacman")}
   pacman::p_load_gh("colinconwell/Coco-Pack-R")

Shell Commands
^^^^^^^^^^^^^^

.. code-block:: bash

   pip install "cocopack[shell]"

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   user/quickstart
   user/installation
   user/cli

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/python/index
   api/shell/index

.. toctree::
   :maxdepth: 1
   :caption: Development
   
   dev/contributing
   dev/release_notes

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`