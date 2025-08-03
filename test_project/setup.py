from setuptools import setup, find_packages

setup(
    name="test-project",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.28.0",
        "flask>=2.2.0",
        "jinja2>=3.1.0",
    ],
    python_requires=">=3.8",
) 