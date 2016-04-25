from setuptools import find_packages, setup
import os
import sys

try:
    from Cython.Build import cythonize
except ImportError:
    print('Please install "cython" first')


def get_version():
    with open('VERSION') as f:
        return f.read().strip()

def cython_modules():
    """
    Collects and "cythonizes" all cython modules. If Cython isn't installed 
    then skip.
    """
    try:
        return cythonize('utils/math.pyx')
    except NameError:
        return []


setup(
    name='utils',
    version=get_version(),
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
    license='MIT',
    long_description=open('README.rst').read(),
    author='Michael F Bryan',
    description='My utility scripts',
    ext_modules=cython_modules(),
    install_requires=[
        'cython',
        'pytest',
        'bs4',
        'sphinx',
        'sphinxcontrib-napoleon',
        'invoke',
        'pytest-cov',
        'pylint',
        ],
)
