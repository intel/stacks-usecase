# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.insert(0, os.path.abspath("."))

project = "stacks-usecase"
copyright = "2019, Intel"
author = "unrahul"

# The short X.Y version
version = "0.0.1"
release = version
extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
html_theme = "alabaster"

html_theme_options = {
    "description": "End to End Deep Learning usecases using Intel System Stacks",
    "github_user": "intel",
    "github_repo": "stacks-usecase",
    "github_button": True,
    "travis_button": True,
    "codecov_button": True,
}


master_doc = 'index'
