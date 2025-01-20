# Configuration file for the Sphinx documentation builder.  # noqa: INP001
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys

# Add the parent directory of the documentation root to sys.path
sys.path.insert(0, os.path.abspath("../../src"))

project = "tika-python"
copyright = "2024, Chris A. Mattmann"  # noqa: A001
author = "Chris A. Mattmann"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.todo",
    "sphinx.ext.duration",
    "myst_parser",
    "sphinx.ext.intersphinx",  # Link to other Sphinx docs
    "sphinx_autodoc_typehints",  # Better type hint rendering
    "sphinx.ext.coverage",  # Check documentation coverage
    "sphinx_design",  # Better UI components
    "sphinx_sitemap",  # Generate sitemap
    "sphinx_git",
    "sphinx_copybutton",  # Add copy button to code blocks
    "sphinx.ext.autosummary",  # Generate API docs summaries
    "sphinx_design",  # Add nice UI components
    "sphinxemoji.sphinxemoji",  # Add emoji support
    "sphinx_tabs.tabs",  # Add tabbed content
    "sphinx_togglebutton",  # Add collapsible sections
]

templates_path = ["_templates"]
exclude_patterns = ["test*"]
sphinxemoji_style = "twemoji"


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinxawesome_theme"
html_permalinks_icon = "<span>#</span>"
html_static_path = ["_static"]
