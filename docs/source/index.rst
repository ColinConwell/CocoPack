.. _index:

Welcome to Coco-Pack's Documentation
====================================

.. image:: ../../logo.png
   :width: 150px
   :align: right
   :alt: Coco-Pack Logo

Coco-Pack is a collection of programmatic toolkits for Python, R, and shell scripting. It provides a unified set of utilities to streamline your development workflow across multiple languages.

.. note::

   This documentation is under active development.

Features
--------

* **Python Utilities**: Tools for data processing, visualization, and automation
* **Shell Scripts**: Command-line utilities for everyday tasks
* **R Package**: Statistical and data manipulation tools
* **Cross-language Interoperability**: Seamless workflow between languages

Quick Start
-----------

Python Package
^^^^^^^^^^^^^

.. code-block:: bash

   pip install coco-pack

R Package
^^^^^^^^^

.. code-block:: R

   if (!require(pacman)) {install.packages("pacman")}
   pacman::p_load_gh("colinconwell/Coco-Pack-R")

Shell Commands
^^^^^^^^^^^^^

.. code-block:: bash

   pip install "coco-pack[shell]"

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   user/installation
   user/quickstart
   user/shell_usage
   user/python_usage
   user/r_usage

.. toctree::
   :maxdepth: 2
   :caption: API Reference
   
   api/python/index
   api/shell/index
   api/r/index

.. toctree::
   :maxdepth: 1
   :caption: Development
   
   dev/contributing
   dev/release_notes

Indices and tables
=================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`