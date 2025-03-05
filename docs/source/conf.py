import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath('../..'))
# Add the python directory for direct python imports
sys.path.insert(0, os.path.abspath('../../python'))
from python.cocopack import __version__

# -- Project information -----------------------------------------------------
project = 'Coco-Pack'
copyright = '2025, Colin Conwell'
author = 'Colin Conwell'
version = __version__
release = __version__

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosummary',
    'myst_parser',
    'sphinx_copybutton',
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = []
source_suffix = ['.rst', '.md']
master_doc = 'index'

# Enable autodoc to import the package
autodoc_member_order = 'bysource'
autoclass_content = 'both'
autodoc_typehints = 'description'
autodoc_typehints_format = 'short'

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True

# Intersphinx settings
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_logo = '../../logo.png'
html_static_path = ['_static']
html_css_files = ['custom.css']
html_js_files = ['custom.js']
# Using custom layout.html template to override title for all pages

html_sidebars = {"**": []}

# PyData theme options
html_theme_options = {
    "logo": {
        "text": "Coco-Pack",
        "image_light": "../../logo.png",
        "image_dark": "../../logo.png",
        "alt_text": "Coco-Pack",
    },
    "github_url": "https://github.com/ColinConwell/Coco-Pack",
    "use_edit_page_button": True,
    "navigation_with_keys": True,
    "announcement": "This documentation is under active development.",
    "show_toc_level": 2,
    "icon_links": [
        {
            "name": "Documentation Source",
            "url": "https://github.com/ColinConwell/Coco-Pack/tree/main/docs/source",
            "icon": "fa-book",
        },
    ],
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "search_bar_position": "none",  # Disable the search bar
    "footer_items": ["copyright", "last-updated"],
    "secondary_sidebar_items": ["page-toc", "edit-this-page"],
    "pygment_light_style": "tango",
    "pygment_dark_style": "monokai",
}

# Link to GitHub source
html_context = {
    "github_user": "ColinConwell",
    "github_repo": "Coco-Pack",
    "github_version": "main",
    "doc_path": "docs/source",
}

# Syntax highlighting
pygments_style = 'sphinx'