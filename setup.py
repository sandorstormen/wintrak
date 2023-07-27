from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name="wintrak",
    packages=find_packages(exclude=("gui", "Notebooks")),
)
