#!/usr/bin/env python3
"""
Shotux setup.py for pip installation
"""

from setuptools import setup, find_packages
import os

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="shotux",
    version="1.0.0",
    author="Shotux Developer",
    author_email="developer@example.com",
    description="A comprehensive screenshot tool for Linux with GUI support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Loofn/shotux",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Capture :: Screen Capture",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: POSIX :: Linux",
        "Environment :: X11 Applications",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "shotux=shotux.main:main",
            "shotux-cli=shotux.cli:main",
        ],
        "gui_scripts": [
            "shotux-gui=shotux.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "shotux": ["*.md", "*.txt"],
    },
    data_files=[
        ("share/applications", ["data/shotux.desktop"]),
        ("share/pixmaps", ["data/shotux.png"]),
        ("share/doc/shotux", ["README.md"]),
    ],
    zip_safe=False,
)
