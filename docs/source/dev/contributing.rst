.. _contributing:

============
Contributing
============

We welcome contributions to Coco-Pack! This guide will help you get started.

Development Setup
===============

1. Clone the repository:

   .. code-block:: bash

       git clone https://github.com/ColinConwell/Coco-Pack.git
       cd Coco-Pack

2. Install development dependencies:

   .. code-block:: bash

       pip install -e ".[dev]"

3. Install documentation dependencies:

   .. code-block:: bash
   
       pip install -e ".[docs]"

Coding Standards
==============

- We use Black for code formatting
- We use isort for import sorting
- We use mypy for type checking

You can run these tools with:

.. code-block:: bash

    # Format code
    black python/cocopack
    
    # Sort imports
    isort python/cocopack
    
    # Type checking
    mypy python/cocopack

Testing
======

We use pytest for testing. Run the tests with:

.. code-block:: bash

    pytest

Pull Requests
===========

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

Please include:

- A clear description of the changes
- Tests for new functionality
- Documentation updates if needed

Documentation
===========

To build the documentation locally:

.. code-block:: bash

    cd docs
    make html

Then open ``build/html/index.html`` in your browser.