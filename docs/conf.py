import os
import sys


sys.path.insert(0, os.path.abspath("../src"))

project = "beautiful"
author = "Tai Hui"
copyright = f"2022, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]
