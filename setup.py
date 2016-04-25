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


def increment_version():
    """
    Increment the minor version number and then write it to the version.py 
    file.

    Returns
    -------
    str
        The new version number 
    """ 
    version_info = [int(a) for a in get_version().split('.')] 
    version_info[-1] += 1
    new_version = '.'.join(str(a) for a in version_info)

    # Write the new version to the version.py file
    with open('VERSION', 'w') as f:
        f.write(new_version)

    return new_version


# Add a `python setup.py tag` command that will increment the current version
# And then do `git tag ...`
if sys.argv[-1] == 'tag':
    version = increment_version()

    command = "git tag -a 'v%s' -m 'version %s'" % (version, version)
    print(command)
    os.system(command)

    command = "git push --tags"
    print(command)
    os.system(command)

    sys.exit()


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
        'pytest',
        'bs4',
        'sphinx',
        'sphinxcontrib-napoleon',
        'invoke',
        'pytest-cov',
        'pylint',
        ],
)
