# Code Documentation Guide

- [Docs with `pdoc`](#docs-with-pdoc)
- [Docs with Sphinx](#docs-with-sphinx)
  - [Build Commands](#build-commands)
  - [Auto-Doc Setup](#auto-doc-setup)
    - [Autosummary](#autosummary)
    - [Auto-Gen](#auto-gen)
    - [API-Docs](#api-docs)
    - [Makefile](#makefile)
  - [Auto-Doc Details](#auto-doc-details)
    - [Settings](#settings)
    - [Error Handling](#error-handling)
  - [Myst Markdown](#myst-markdown)
  - [Sphinx Themes](#sphinx-themes)
    - [Book Theme:](#book-theme)
    - [Sphinx Gallery](#sphinx-gallery)
  - [Sphinx Extensions](#sphinx-extensions)
    - [Napoleon](#napoleon)
  - [GitHub Pages](#github-pages)
    - [Workflow Spec](#workflow-spec)
  - [Local Testing](#local-testing)

## Docs with [`pdoc`](https://pdoc.dev/docs/cli.html)

By far, the fastest, easiest way to generate documentation for your code is with `pdoc`, which will build a walkthrough of your API with two commands (one of which is installation):

```bash
pip install pdoc
```

```bash
pdoc --html --output-dir docs/
```

## Docs with Sphinx

### Build Commands

Assuming we have a `Makefile`:

```bash
make clean
make html
```

Or, altogether in one line:

```bash
make clean && make html
```

### Auto-Doc Setup

Sphinx has multiple ways of automatically generating documentation from existing code.

#### Autosummary

**conf.py** specifications:

```python
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
]

```
#### Auto-Gen 

The following will `auto-gen` target doc files:

```bash
sphinx-autogen -o generated *.rst
```

- `-o`, `--output-dir DIR`: The directory to place all output.
- `-s`, `--suffix SUFFIX`: Default suffix for files (default: .rst).
- `-t`, `--templates TEMPLATE_DIR`: Custom template directory.
- `-d`, `--maxdepth DEPTH`: Specify the maximum depth of the table of contents tree. The default is -1, meaning no limit.
- `-i`, `--no-toc`: Prevents the generation of a table of contents file.
- `-f`, `--force`: Forces overwriting existing files.
- `-l`, `--follow-links`: Follow symbolic links when searching for source files.
- `-n`, `--dry-run`: Performs a dry run that doesn't write any files but shows what would have been created.
- `-M`: Puts modules first (before submodules).

#### API-Docs

```bash
sphinx-apidoc -a -f -o source ../ezpandas -M -t _templates
```
`-o`: specifies the doc output directory<br>
`-t`: specifies the doc template directory<br>
`-f`: forces regeneration of the docs<br>
`-M`: puts modules first (before submodules)<br>

#### Makefile

Auto-documentation functionality can also be achieved by modifying `Makefile`.

**API-Doc** `Makefile` specs:

```Makefile
# -------------------------------------------
# Alternative specification for sphinx-apidoc

SPHINXAPIDOC   = sphinx-apidoc
SOURCEDIR      = ../ezpandas
BUILDDIR       = _build

.PHONY: apidoc
apidoc:
    $(SPHINXAPIDOC) -f -o $(BUILDDIR)/source $(SOURCEDIR)

html: apidoc
    @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

### Auto-Doc Details

#### Settings

Other autodoc settings include (e.g.):

* `exclude-members`

#### Error Handling

**conf.py** can be modified with further settings that more gracefully handle parsing errors (e.g.):

```python
nitpicky = False
suppress_warnings = ['autodoc', 'autodoc.import_object', 'autodoc.warning']
```

### Myst Markdown

Sphinx can convert Markdown to reStructuredText (RST) using Myst.

```shell
pip install myst-parser
```

**conf.py** specifications:

```python
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
```

### Sphinx Themes

Browse the [Sphinx Theme Gallery](https://sphinx-themes.org/).

- [Book Theme](https://sphinx-themes.org/sample-sites/sphinx-book-theme/): `pip install sphinx-book-theme`
- [Awesome](https://sphinx-themes.org/sample-sites/sphinxawesome-theme/): `pip install sphinxawesome-theme`
- [Wagtail](https://sphinx-themes.org/sample-sites/sphinx-wagtail-theme/): `pip install sphinx-wagtail-theme`
- [Nefertiti](https://sphinx-themes.org/sample-sites/sphinx-nefertiti/): `pip install sphinx-nefertiti`
- [PyData Theme](https://sphinx-themes.org/sample-sites/pydata-sphinx-theme/): `pip install pydata-sphinx-theme`

To install all of these themes at once, run:

```bash
pip install sphinx-book-theme sphinxawesome-theme sphinx-wagtail-theme sphinx-nefertiti
```

More `sphinx-awesome` documentation available at [sphinxawesome.xyz](https://sphinxawesome.xyz/) and on [GitHub](https://github.com/kai687/sphinxawesome-theme)

#### Book Theme:

```bash
pip install sphinx-book-theme
```

**Primary Settings** [[Source](https://github.com/executablebooks/sphinx-book-theme/blob/master/docs/reference.md)]:

* `path_to_docs` (string): Path to the documentation files, relative to the repository root (e.g. `docs/`).
* `repository_url` (string): URL of the repository for the documentation (e.g. the GitHub repository URL).
* `repository_branch` (string): Branch of the repository for the documentation (e.g., `master`, `main`, `docs`).
* `use_issues_button` (bool): Add an button in the header with a link to issues for the repository.
* `use_download_button` (bool): Add a button in the header to download the source file of the page.
* `use_fullscreen_button` (bool): Add a button in the header to trigger full-screen mode.
* `use_repository_button` (bool): Add a button in the header that links to the repository of the documentation.
* `launch_buttons` (bool): Include Binder launch buttons for pages that were built from Jupyter Notebooks.
* `home_page_in_toc` (bool): Whether to put the home page in the Navigation Bar (at the top).
* `show_navbar_depth` (int): Show children in the navigation bar down to the depth listed here.
* `max_navbar_depth` (int): The maximum number of levels to show in the navbar. (4 is default)
* `collapse_navbar` (bool): Whether to collapse the navbar, stopping the tree from being expanded. (False is default)
* `extra_navbar` (str): Extra HTML to add below the sidebar footer.
* `extra_footer` (str): Extra HTML to add in the footer of each page.
* `toc_title` (str): The text to be displayed with the in-page TOC (`Contents` is default)

#### Sphinx Gallery

See theme options in vivo using [Sphinx-Gallery](https://sphinx-gallery.github.io/stable/index.html).

```bash
pip install sphinx-gallery
```

### Sphinx Extensions

Examples: 
- intersphinx
- mathjax
- ifconfig

#### Napoleon

For auto-doc from google and numpy doc formats.

**Settings**:

```python
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
# napoleon_include_private_with_doc = True
# napoleon_include_special_with_doc = True
# napoleon_use_ivar = True
# napoleon_use_param = True
# napoleon_use_rtype = True
```
### GitHub Pages

If publishing Sphinx-generated docs to GitHub pages, there are a few additional considerations.

#### Workflow Spec

**Consideration**: We may need to copy the code during the creation of the GitHub pages if we want autosummary to work:

```yml
- name: Copy package code
  run: |
    cp -r package_dir ../
```

The version below just copies .py files.

```yml
- name: Copy package code
  run: |
    mkdir -p ../package_dir
    find package_dir -name "*.py" -exec cp {} ../package_dir \;
```

### Local Testing

Local testing of GitHub Pages can be done using Ruby.

```bash
gem install jekyll webrick
bundle init
echo 'gem "github-pages", group: :jekyll_plugins' >> Gemfile
bundle install
bundle exec jekyll serve
```

To make sure that the Gemfile exists before writing in new lines, you can run:

```bash
bashgrep -qxF 'gem "github-pages", group: :jekyll_plugins' Gemfile || echo 'gem "github-pages", group: :jekyll_plugins' >> Gemfile
```

A GitHub workflow for local testing might look like this:

```yml
name: Test GitHub Pages Build

on:
  push:
    paths:
      - 'sphinx/**'
  pull_request:
    paths:
      - 'sphinx/**'

jobs:
  test-build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Ruby
      uses: ruby/setup-ruby@v1
      with:
        ruby-version: '2.7'
    - name: Install dependencies
      run: |
        cd sphinx
        bundle install
    - name: Build site
      run: |
        cd sphinx
        bundle exec jekyll build
```