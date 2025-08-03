#!/usr/bin/env python3
"""
Setup для Deprecated Checker.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_path = Path(__file__).parent / "README.md"
long_description = ""
if readme_path.exists():
    with open(readme_path, "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements_path = Path(__file__).parent / "requirements.txt"
install_requires = []
if requirements_path.exists():
    with open(requirements_path, "r", encoding="utf-8") as f:
        install_requires = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="deprecated-checker",
    version="1.0.0",
    author="Iulian Pavlov",
    author_email="iulianpavlov@icloud.com",
    description="Tool for checking deprecated dependencies in Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/julicq/deprecated-checker",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            "deprecated-checker=deprecated_checker:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["data/*.yaml"],
    },
    keywords="python dependencies deprecated security audit",
    project_urls={
        "Bug Reports": "https://github.com/julicq/deprecated-checker/issues",
        "Source": "https://github.com/julicq/deprecated-checker",
        "Documentation": "https://github.com/julicq/deprecated-checker#readme",
    },
) 