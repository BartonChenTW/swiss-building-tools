from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="swiss-building-tools",
    version="0.1.3",
    author="Barton Chen",
    author_email="barton.chen.energy@gmail.com",
    description="Tools for processing Swiss building data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BartonChenTW/swiss-building-tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "requests>=2.25.0",
    ],
)