===============
My Utils README
===============

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
    venv my_virtual_env
or, ::

    mkvirtualenv my_virtual_env

Then finally, install the package::
    python setup.py install

