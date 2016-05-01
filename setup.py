from setuptools import find_packages, setup
import os
import sys

try:
    from Cython.Build import cythonize
except ImportError:
    print('Please install "cython" first')
    sys.exit(1)


def get_version():
    with open('VERSION') as f:
        return f.read().strip()


setup(
    name='utils',
    version=get_version(),
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
    license='MIT',
    long_description=open('README.rst').read(),
    author='Michael F Bryan',
    description='My utility scripts',
    ext_modules=cythonize('utils/math.pyx'),
    install_requires=[
        'cython',
        'bs4',
        'sphinx',
        'sphinxcontrib-napoleon',
        'invoke',
        'pylint',
        ],
)
