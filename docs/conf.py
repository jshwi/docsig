# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.append(os.path.abspath("./extensions"))


# -- Project information -----------------------------------------------------

project = "docsig"
copyright = "2026, Stephen Whitlock"
author = "Stephen Whitlock"

# The full version, including alpha/beta/rc tags
release = "0.91.4"

# SEO-friendly project description, rendered into meta tags by
# _templates/base.html
description = """\
docsig is a Python tool for checking signature parameters in docstrings.
 Ensures proper documentation of function and method parameters for Sphinx,
 NumPy, and Google docstring formats. Use as a standalone tool, flake8 plugin,
 or pre-commit hook to maintain accurate Python documentation.
"""

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.imgmath",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "myst_parser",
    "sphinx_copybutton",
    "generate",
    "sphinx_sitemap",
    "files",
    "jsonschema",
]

sitemap_url_scheme = "{lang}latest/{link}"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
# Files only ever pulled in with `.. include::` are excluded so they are
# not also built as standalone duplicate pages.
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "_generated",
    "docsig.rst",
    "usage/classes.rst",
    "usage/editor.rst",
    "usage/check-configuration.rst",
    "usage/ignore-configuration.rst",
    "usage/*-messages.rst",
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_dark_style = "monokai"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages. See the documentation for
# a list of builtin themes.
#
html_theme = "furo"
html_domain_indices = True
html_use_index = True
html_show_sourcelink = True
html_show_sphinx = False
myst_heading_anchors = 3
# keep `.. todo::` development notes out of the published site
todo_include_todos = False
html_logo = "static/docsig.svg"
html_favicon = "static/favicon.ico"

# SEO Configuration
html_baseurl = "https://docsig.io/"

# Variables for the SEO meta tags rendered by _templates/base.html
html_context = {
    "seo_description": " ".join(description.split()),
    "seo_author": author,
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
