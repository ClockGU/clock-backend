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

import django

sys.path.insert(0, os.path.abspath("."))
FILE_PATH = os.path.dirname(__file__)
path = FILE_PATH[: FILE_PATH.rfind("/")]
prev_path = path[: path.rfind("/")]

sys.path.append(prev_path)

sys.path.insert(0, os.path.abspath(".."))

os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"
os.environ["DJANGO_SECRET_KEY"] = "h18i_1j3^d1e6iq8xur&yvbkpk08il9x^&9cf2l2%-0yqx7ss)"
os.environ["POSTGRES_HOST"] = "db"
os.environ["POSTGRES_PORT"] = "5432"
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings.local"
os.environ["RABBITMQ_URL"] = "amqp://broker_adm:broker_pass@rabbit_broker:5672/"
django.setup()


# -- Project information -----------------------------------------------------

project = "Clock-Backend"
copyright = "2022, Christian Grossmüller"
author = "Christian Grossmüller"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
]
autodoc_default_flags = ["members"]
autosummary_generate = True
# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["**/migrations*"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]
