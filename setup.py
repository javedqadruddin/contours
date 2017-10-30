"""Setup for person2vec
"""
import sys

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requirements = []
    for line in f:
        requirements.append(line.strip())

setup(
    name='contours',

    version='0.1',

    description='pipeline to deliver batches of dicom-image-derived data and contour masks for training machine learning models ',
    long_description=long_description,

    # The project's main homepage.
    url='https://github.com/javedqadruddin/contours',

    # Author details
    author='JQ',
    author_email='jqjunk@gmail.com',

    license='copyright protected',

    packages=find_packages(exclude=['tests']),

    install_requires=requirements

)
