from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

setup(
    name="wintrak",
    packages=find_packages(
        exclude=("tests",),
    ),
    entry_points={
        "console_scripts": [
            "wintrak = wintrak.main:run",
        ],
    },
    install_requires=[
        "Xlib",
    ],
)
