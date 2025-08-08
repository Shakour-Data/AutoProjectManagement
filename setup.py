#!/usr/bin/env python3
"""
Setup script for AutoProjectManagement
"""

from setuptools import setup, find_packages

# Read the README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements
with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="autoprojectmanagement",
    version="1.0.0",
    author="AutoProjectManagement Team",
    author_email="team@autoprojectmanagement.com",
    description="Automated project management system for software development workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/autoprojectmanagement/autoprojectmanagement",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Project Management",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "apm=autoprojectmanagement.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "autoprojectmanagement": ["templates/*", "config/*"],
    },
)
