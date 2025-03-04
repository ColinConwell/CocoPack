.. _index:

Welcome to Coco-Pack's Documentation
====================================

.. image:: ../../logo.png
   :width: 180px
   :align: right
   :alt: Coco-Pack Logo

Coco-Pack is a collection of programmatic toolkits for Python, R, and shell scripting. It provides a unified set of utilities to streamline your development workflow across multiple languages.

.. note::

   *Caveat Emptor*: This package is under active development. All code has been tested by a human (me), but I've made ample use of a custom generative AI pipeline for (auto-)documentation. If the documentation appears inaccurate, please refer to the source code or file an issue to let me know.

Features
--------

* **Python Utilities**: Tools for data processing, visualization, and automation
* **Shell CLI**: Command-line tools for common tasks and workflows
* **R Package**: Tools for statistics, data manipulation, and visualization

Quick Start
-----------

Python Package
^^^^^^^^^^^^^^

.. code-block:: bash

   pip install coco-pack

R Package
^^^^^^^^^

.. code-block:: R

   if (!require(pacman)) {install.packages("pacman")}
   pacman::p_load_gh("colinconwell/Coco-Pack-R")

Shell Commands
^^^^^^^^^^^^^^

.. code-block:: bash

   pip install "coco-pack[shell]"

Contents
--------

.. toctree::
   :maxdepth: 2
   :caption: User Guide
   
   user/quickstart
   user/installation

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

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`