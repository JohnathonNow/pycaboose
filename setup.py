#!/usr/bin/env python3
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pycaboose',
    version='1.1.0',
    author='John Westhoff',
    author_email='johnjwesthoff@gmail.com',
    description=('A python library for persisting data within a script.'),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/JohnathonNow/pycaboose',
    packages=setuptools.find_packages(),
    test_suite='tests',
    include_package_data=True,
)
