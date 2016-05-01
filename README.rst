===============
My Utils README
===============

.. Circle.ci build status
.. image:: https://circleci.com/gh/Michael-F-Bryan/mfb_utils.svg?style=svg
    :target: https://circleci.com/gh/Michael-F-Bryan/mfb_utils

.. Tag number
.. image:: https://img.shields.io/github/tag/Michael-F-Bryan/mfb_utils.svg?maxAge=2592000

.. License
.. image:: https://img.shields.io/github/license/Michael-F-Bryan/mfb_utils.svg?maxAge=2592000

Description
===========
A bunch of commonly used functions, classes and decorators that I've bundled up
into one module. A particular favourite of mine is the Hook decorator, a
decorator that you can apply to any method that will automatically call another
function before or after the wrapped function is called.

A particular use case could be to give a framework developer the ability to 
add hooks to their framework with minimal effort.

Installing
==========
First make sure to clone the repo from github::
    git clone https://github.com/Michael-F-Bryan/mfb_utils.git

(Optional) Next make a virtual environment with either virtualenv or
virtualenvwrapper::

    python -m venv my_virtual_env

or, ::

    mkvirtualenv my_virtual_env

Make sure `Cython` is installed (may require root privileges)::

    pip install cython

Then finally, install the package::

    python setup.py install

Testing
=======
Testing is done using the py.test framework. Simply run `py.test` from the
project's root directory to run all the tests for this package.
