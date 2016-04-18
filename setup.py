from setuptools import find_packages, setup
from Cython.Build import cythonize
import os
import sys
from version import __version__


def increment_version():
    version_info = [int(a) for a in __version__.split('.')]
    version_info[-1] += 1
    new_version = '.'.join(version_info)

    # Write the new version to the version.py file
    with open('version.py', 'w') as f:
        f.write('__version__ = {}'.format(new_version))

    return new_version


# Add a `python setup.py tag` command that will increment the current version
# And then do `git tag ...`
if sys.argv[-1] == 'tag':
    version = increment_version()
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()


setup(
    name='utils',
    version=__version__,
    packages=find_packages(exclude=['tests', 'docs', 'scripts']),
    license='MIT',
    long_description=open('README.rst').read(),
    author='Michael F Bryan',
    description='My utility scripts',
    ext_modules=cythonize('utils/math.pyx'),
    install_requires=[
        'cython',
        'pytest',
        'bs4',
        'sphinx',
        'sphinxcontrib-napoleon',
        ],
)
