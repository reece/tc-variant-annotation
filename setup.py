import os
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as readme:
    README = readme.read()

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='tc_variant-annotation',
    description='Variant Annotation Technical Challenge',
    version='0.0.1',
    long_description=README,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=required,
)
